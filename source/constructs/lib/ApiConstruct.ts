import path = require('path');
import { Aws, Duration, CfnOutput } from 'aws-cdk-lib';
import { RestApi, EndpointType, Cors, LambdaIntegration, Deployment, MethodLoggingLevel, Stage } from 'aws-cdk-lib/aws-apigateway';
import { Policy, PolicyStatement, Role, ServicePrincipal } from 'aws-cdk-lib/aws-iam';
import { Code, LayerVersion, Runtime, Function } from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import { BuildConfig } from './common/BuildConfig';
import { SolutionInfo } from './common/SolutionInfo';


export class ApiConstruct extends Construct {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    const role = this.createRole();
    const layerVersion = this.createLayerVersion();
    const apiFunction = this.createFunction(role, layerVersion);
    this.createApiGateway(apiFunction);
  }

  private createRole() {
    const apiRole = new Role(this, 'APIRole', {
      roleName: `${SolutionInfo.SOLUTION_NAME}APIRole-${Aws.REGION}`,
      assumedBy: new ServicePrincipal('lambda.amazonaws.com'),
    });

    const logPolicy = new Policy(this, 'LogPolicy', {
      policyName: `${SolutionInfo.SOLUTION_NAME}LogPolicy`,
      statements: [
        new PolicyStatement({
          actions: [
            'logs:CreateLogGroup',
            'logs:CreateLogStream',
            'logs:PutLogEvents',
            'logs:DescribeLogGroups',
            'logs:FilterLogEvents',
          ],
          resources: ['*'],
        }),
      ],
    });
    apiRole.attachInlinePolicy(logPolicy);

    const apiPolicy = new Policy(this, 'ApiPolicy', {
      policyName: `${SolutionInfo.SOLUTION_NAME}ApiPolicy`,
      statements: [
        new PolicyStatement({
          actions: [
            'dynamodb:*',
          ],
          resources: [`arn:${Aws.PARTITION}:dynamodb:${Aws.REGION}:${Aws.ACCOUNT_ID}:table/PetSample`],
        }),
      ],
    });
    apiRole.attachInlinePolicy(apiPolicy);
    return apiRole;
  }

  private createLayerVersion() {
    const apiLayerVersion = new LayerVersion(this, 'APILayer', {
      code: Code.fromAsset(path.join(__dirname, '../../api'), {
        bundling: {
          image: Runtime.PYTHON_3_12.bundlingImage,
          command: [
            'bash',
            '-c',
            `pip install -r requirements.txt ${BuildConfig.PIP_PARAMETER} -t /asset-output/python`,
          ],
        },
      }),
      layerVersionName: `${SolutionInfo.SOLUTION_NAME}-API`,
      compatibleRuntimes: [Runtime.PYTHON_3_12],
      description: `${SolutionInfo.SOLUTION_FULL_NAME} - API layer`,
    });
    return apiLayerVersion;
  }

  private createFunction(apiRole: Role, apiLayerVersion: LayerVersion) {
    const apiFunction = new Function(this, 'ApiFunction', {
      functionName: `${SolutionInfo.SOLUTION_NAME}-API`,
      description: `${SolutionInfo.SOLUTION_FULL_NAME} - API`,
      runtime: Runtime.PYTHON_3_12,
      handler: 'main.handler',
      code: Code.fromAsset(path.join(__dirname, '../../api')),
      memorySize: 1024,
      timeout: Duration.minutes(2),
      layers: [apiLayerVersion],
      role: apiRole,
      environment: {
        Stage: SolutionInfo.STAGE_VALUE,
      },
    });
    return apiFunction;
  }

  private createApiGateway(apiFunction: Function) {
    const api = new RestApi(this, 'ApiGateway', {
      restApiName: 'FastAPI sample',
      description: 'FastAPI sample',
      deploy: false,
      endpointConfiguration: {
        types: [EndpointType.REGIONAL],
      },
      defaultCorsPreflightOptions: {
        allowHeaders: [
          'Content-Type',
          'X-Amz-Date',
          'Authorization',
          'X-Api-Key',
        ],
        allowMethods: ['GET', 'POST', 'OPTION'],
        allowCredentials: true,
        allowOrigins: Cors.ALL_ORIGINS,
      },
    });

    const resource = api.root;
    resource.addProxy({
      anyMethod: true,
      defaultIntegration: new LambdaIntegration(apiFunction, { proxy: true }),
    });

    resource.addMethod('GET',
      new LambdaIntegration(apiFunction, { proxy: true }),
    );

    const deployment = new Deployment(this, 'ApiGatewayDeployment', {
      api: api,
    });

    const deploymentStage = new Stage(this, 'ApiGatewayStage', {
      stageName: SolutionInfo.STAGE_VALUE,
      deployment: deployment,
      dataTraceEnabled: false,
      loggingLevel: MethodLoggingLevel.INFO,
    });

    new CfnOutput(this, 'InvokeBaseUrl', {
      key: 'InvokeBaseUrl',
      value: deploymentStage.urlForPath(),
    });
  }
}

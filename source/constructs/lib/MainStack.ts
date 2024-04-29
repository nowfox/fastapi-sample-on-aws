/**
 *  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
 *  with the License. A copy of the License is located at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES
 *  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions
 *  and limitations under the License.
 */

import {
    CfnOutput,
    CfnParameter,
    CfnResource,
    Stack,
    StackProps,
    CfnCondition,
    Fn,
    CfnStack,
    Tags,
    Aws,
} from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { SolutionInfo } from './common/SolutionInfo';
import { BuildConfig } from './common/BuildConfig';
import { Parameter } from './common/Parameter';
import { ApiStack } from './ApiStack';

export interface MainProps extends StackProps {
    readonly lambdaMemorySize?: number;
}


export class MainStack extends Stack {

    constructor(scope: Construct, id: string, props?: MainProps) {
        super(scope, id, props);

        this.templateOptions.description = SolutionInfo.DESCRIPTION;
        Parameter.init();
        this.setBuildConfig();

        new ApiStack(this, 'API');

        this.templateOptions.metadata = {
            'AWS::CloudFormation::Interface': {
                ParameterGroups: Parameter.paramGroups,
                ParameterLabels: Parameter.paramLabels,
            },
        };

        Tags.of(this).add(SolutionInfo.TAG_KEY, SolutionInfo.TAG_VALUE);
    }

    private setBuildConfig() {
        BuildConfig.PIP_PARAMETER = this.node.tryGetContext('PipParameter') ?? '';
    }

}

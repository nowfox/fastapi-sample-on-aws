import { Construct } from 'constructs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';


export class DdbConstruct extends Construct {
    constructor(scope: Construct, id: string) {
        super(scope, id);

        new dynamodb.Table(this, 'PetTable', {
            tableName: "PetSample",
            partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
            billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
        });
    }
}
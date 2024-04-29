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

export class SolutionInfo {
    static SOLUTION_ID = 'Sxxxxx';
    static SOLUTION_FULL_NAME = 'BaseFastAPIProject';
    static SOLUTION_NAME = 'BaseFastAPI';
    static SOLUTION_VERSION = '@TEMPLATE_BUILD_VERSION@';
    static DESCRIPTION = `(${SolutionInfo.SOLUTION_ID}) ${SolutionInfo.SOLUTION_FULL_NAME} (Version ${SolutionInfo.SOLUTION_VERSION})`;
    static TAG_NAME = 'Name';
    static TAG_KEY = 'Owner';
    static TAG_VALUE = SolutionInfo.SOLUTION_NAME;
    static STAGE_VALUE = 'demo';
}

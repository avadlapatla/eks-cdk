from aws_cdk import (
    core as cdk,
    aws_eks as eks,
    aws_iam as iam,
)
# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.


class EksCdkStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cluster_admin = iam.Role(
            self, 'ClusterAdmin',
            assumed_by= iam.AccountRootPrincipal(),
            role_name= 'eks_cdk_admin'
        )

        # The code that defines your stack goes here
        example_cluster = eks.Cluster(
            self, 'Example',
            version= eks.KubernetesVersion.V1_19,
            masters_role= cluster_admin
        )

        example_cluster.aws_auth.add_user_mapping(
            user= iam.User.from_user_name(self, 'K8SUser', 'k8s' ),
            groups= ['system:masters']
        )

        example_cluster.add_fargate_profile(   
            'ExampleFargate',
            selectors = [
                {
                    'namespace': 'kube-system'
                }
            ],
            fargate_profile_name = 'ExampleFargate'
        )
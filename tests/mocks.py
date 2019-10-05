all_projects = \
[
    {
        'Id': 'Projects-1',
        'VariableSetId': 'variableset-Projects-1',
        'DeploymentProcessId': 'deploymentprocess-Projects-1',
        'ClonedFromProjectId': None,
        'DiscreteChannelRelease': False,
        'IncludedLibraryVariableSetIds': [],
        'DefaultToSkipIfAlreadyInstalled': False,
        'TenantedDeploymentMode': 'Untenanted',
        'DefaultGuidedFailureMode': 'EnvironmentDefault',
        'VersioningStrategy': {
            'Template': '#{Octopus.Version.LastMajor}.#{Octopus.Version.LastMinor}.#{Octopus.Version.NextPatch}',
            'DonorPackage': None,
            'DonorPackageStepId': None
        },
        'ReleaseCreationStrategy': {
            'ChannelId': None,
            'ReleaseCreationPackage': None,
            'ReleaseCreationPackageStepId': None
        },
        'Templates': [],
        'AutoDeployReleaseOverrides': [],
        'ReleaseNotesTemplate': None,
        'SpaceId': 'Spaces-1',
        'ExtensionSettings': [],
        'Name': 'test-proj',
        'Slug': 'test-proj',
        'Description': '',
        'IsDisabled': False,
        'ProjectGroupId': 'ProjectGroups-1',
        'LifecycleId': 'Lifecycles-1',
        'AutoCreateRelease': False,
        'ProjectConnectivityPolicy': {
            'SkipMachineBehavior': 'None',
            'TargetRoles': [],
            'AllowDeploymentsToNoTargets': False,
            'ExcludeUnhealthyTargets': False
        },
        'Links': {
            'Self': '/api/Spaces-1/projects/Projects-1',
            'Releases': '/api/Spaces-1/projects/Projects-1/releases{/version}{?skip,take,searchByVersion}',
            'Channels': '/api/Spaces-1/projects/Projects-1/channels{?skip,take,partialName}',
            'Triggers': '/api/Spaces-1/projects/Projects-1/triggers{?skip,take,partialName,triggerActionType}',
            'ScheduledTriggers': '/api/Spaces-1/projects/Projects-1/scheduledtriggers{?skip,take,partialName}',
            'OrderChannels': '/api/Spaces-1/projects/Projects-1/channels/order',
            'Variables': '/api/Spaces-1/variables/variableset-Projects-1',
            'Progression': '/api/Spaces-1/progression/Projects-1{?aggregate}',
            'DeploymentProcess': '/api/Spaces-1/deploymentprocesses/deploymentprocess-Projects-1',
            'Web': '/app#/Spaces-1/projects/Projects-1',
            'Logo': '/api/Spaces-1/projects/Projects-1/logo?cb=2019.8.6',
            'Metadata': '/api/Spaces-1/projects/Projects-1/metadata'
        }
    }
]

created_success = \
{'Id': 'Releases-1',
 'Assembled': '2019-10-06T22:17:45.432+00:00',
 'ReleaseNotes': None,
 'ProjectId': 'Projects-1',
 'ChannelId': 'Channels-1',
 'ProjectVariableSetSnapshotId': 'variableset-Projects-1-s-0-4HDVD',
 'LibraryVariableSetSnapshotIds': [],
 'ProjectDeploymentProcessSnapshotId': 'deploymentprocess-Projects-1-s-1-TUHUR',
 'SelectedPackages': [],
 'PackageMetadata': [],
 'SpaceId': 'Spaces-1',
 'IgnoreChannelRules': False,
 'Version': '1.0.0',
 'LastModifiedOn': '2019-10-06T22:17:46.276+00:00',
 'LastModifiedBy': 'octopus',
 'Links': {'Self': '/api/Spaces-1/releases/Releases-1',
  'Project': '/api/Spaces-1/projects/Projects-1',
  'Progression': '/api/Spaces-1/releases/Releases-1/progression',
  'Deployments': '/api/Spaces-1/releases/Releases-1/deployments{?skip,take}',
  'DeploymentTemplate': '/api/Spaces-1/releases/Releases-1/deployments/template',
  'Artifacts': '/api/Spaces-1/artifacts?regarding=Releases-1',
  'ProjectVariableSnapshot': '/api/Spaces-1/variables/variableset-Projects-1-s-0-4HDVD',
  'ProjectDeploymentProcessSnapshot': '/api/Spaces-1/deploymentprocesses/deploymentprocess-Projects-1-s-1-TUHUR',
  'Web': '/app#/Spaces-1/releases/Releases-1',
  'SnapshotVariables': '/api/Spaces-1/releases/Releases-1/snapshot-variables',
  'Defects': '/api/Spaces-1/releases/Releases-1/defects',
  'ReportDefect': '/api/Spaces-1/releases/Releases-1/defects',
  'ResolveDefect': '/api/Spaces-1/releases/Releases-1/defects/resolve'}}

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .. import (
    Component as _Component_2b0ad27f,
    Project as _Project_57d89203,
    Publisher as _Publisher_8d82749b,
)
from ..github import GithubWorkflow as _GithubWorkflow_a1772357
from ..github.workflows import JobStep as _JobStep_c3287c05
from ..tasks import Task as _Task_fb843092


class Release(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.release.Release",
):
    '''(experimental) Manages releases (currently through GitHub workflows).

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        *,
        task: _Task_fb843092,
        version_json: builtins.str,
        default_release_branch: builtins.str,
        antitamper: typing.Optional[builtins.bool] = None,
        artifacts_directory: typing.Optional[builtins.str] = None,
        initial_version: typing.Optional[builtins.str] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        post_build_steps: typing.Optional[typing.Sequence[_JobStep_c3287c05]] = None,
        prerelease: typing.Optional[builtins.str] = None,
        release_branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        release_every_commit: typing.Optional[builtins.bool] = None,
        release_schedule: typing.Optional[builtins.str] = None,
        release_workflow_setup_steps: typing.Optional[typing.Sequence[_JobStep_c3287c05]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param task: (experimental) The task to execute in order to create the release artifacts. Artifacts are expected to reside under ``artifactsDirectory`` (defaults to ``dist/``) once build is complete.
        :param version_json: (experimental) A name of a .json file to set the ``version`` field in after a bump.
        :param default_release_branch: (experimental) The name of the main release branch. NOTE: this field is temporarily required as we migrate the default value from "master" to "main". Shortly, it will be made optional with "main" as the default. Default: "main"
        :param antitamper: (experimental) Checks that after build there are no modified files on git. Default: true
        :param artifacts_directory: (experimental) A directory which will contain artifacts to be published to npm. Default: "dist"
        :param initial_version: (experimental) The initial version of the repo. The first release will bump over this version, so it will be v0.1.1 or v0.2.0 (depending on whether the first bump is minor or patch). Default: "v0.1.0"
        :param jsii_release_version: (experimental) Version requirement of ``jsii-release`` which is used to publish modules to npm. Default: "latest"
        :param post_build_steps: (experimental) Steps to execute after build as part of the release workflow. Default: []
        :param prerelease: (experimental) Bump as a pre-release (e.g. "beta", "alpha", "pre"). Default: - normal semantic versions
        :param release_branches: (experimental) Branches which trigger a release. Default value is based on defaultReleaseBranch. Default: [ "main" ]
        :param release_every_commit: (experimental) Automatically release new versions every commit to one of branches in ``releaseBranches``. Default: true
        :param release_schedule: (experimental) CRON schedule to trigger new releases. Default: - no scheduled releases
        :param release_workflow_setup_steps: (experimental) A set of workflow steps to execute in order to setup the workflow container.
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image

        :stability: experimental
        '''
        options = ReleaseOptions(
            task=task,
            version_json=version_json,
            default_release_branch=default_release_branch,
            antitamper=antitamper,
            artifacts_directory=artifacts_directory,
            initial_version=initial_version,
            jsii_release_version=jsii_release_version,
            post_build_steps=post_build_steps,
            prerelease=prerelease,
            release_branches=release_branches,
            release_every_commit=release_every_commit,
            release_schedule=release_schedule,
            release_workflow_setup_steps=release_workflow_setup_steps,
            workflow_container_image=workflow_container_image,
        )

        jsii.create(Release, self, [project, options])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> _Publisher_8d82749b:
        '''(experimental) The publisher - responsible for publishing jobs in the workflow.

        :stability: experimental
        '''
        return typing.cast(_Publisher_8d82749b, jsii.get(self, "publisher"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workflow")
    def workflow(self) -> _GithubWorkflow_a1772357:
        '''(experimental) The release workflow.

        :stability: experimental
        '''
        return typing.cast(_GithubWorkflow_a1772357, jsii.get(self, "workflow"))


@jsii.data_type(
    jsii_type="projen.release.ReleaseProjectOptions",
    jsii_struct_bases=[],
    name_mapping={
        "default_release_branch": "defaultReleaseBranch",
        "antitamper": "antitamper",
        "artifacts_directory": "artifactsDirectory",
        "initial_version": "initialVersion",
        "jsii_release_version": "jsiiReleaseVersion",
        "post_build_steps": "postBuildSteps",
        "prerelease": "prerelease",
        "release_branches": "releaseBranches",
        "release_every_commit": "releaseEveryCommit",
        "release_schedule": "releaseSchedule",
        "release_workflow_setup_steps": "releaseWorkflowSetupSteps",
        "workflow_container_image": "workflowContainerImage",
    },
)
class ReleaseProjectOptions:
    def __init__(
        self,
        *,
        default_release_branch: builtins.str,
        antitamper: typing.Optional[builtins.bool] = None,
        artifacts_directory: typing.Optional[builtins.str] = None,
        initial_version: typing.Optional[builtins.str] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        post_build_steps: typing.Optional[typing.Sequence[_JobStep_c3287c05]] = None,
        prerelease: typing.Optional[builtins.str] = None,
        release_branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        release_every_commit: typing.Optional[builtins.bool] = None,
        release_schedule: typing.Optional[builtins.str] = None,
        release_workflow_setup_steps: typing.Optional[typing.Sequence[_JobStep_c3287c05]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for ``Release``.

        :param default_release_branch: (experimental) The name of the main release branch. NOTE: this field is temporarily required as we migrate the default value from "master" to "main". Shortly, it will be made optional with "main" as the default. Default: "main"
        :param antitamper: (experimental) Checks that after build there are no modified files on git. Default: true
        :param artifacts_directory: (experimental) A directory which will contain artifacts to be published to npm. Default: "dist"
        :param initial_version: (experimental) The initial version of the repo. The first release will bump over this version, so it will be v0.1.1 or v0.2.0 (depending on whether the first bump is minor or patch). Default: "v0.1.0"
        :param jsii_release_version: (experimental) Version requirement of ``jsii-release`` which is used to publish modules to npm. Default: "latest"
        :param post_build_steps: (experimental) Steps to execute after build as part of the release workflow. Default: []
        :param prerelease: (experimental) Bump as a pre-release (e.g. "beta", "alpha", "pre"). Default: - normal semantic versions
        :param release_branches: (experimental) Branches which trigger a release. Default value is based on defaultReleaseBranch. Default: [ "main" ]
        :param release_every_commit: (experimental) Automatically release new versions every commit to one of branches in ``releaseBranches``. Default: true
        :param release_schedule: (experimental) CRON schedule to trigger new releases. Default: - no scheduled releases
        :param release_workflow_setup_steps: (experimental) A set of workflow steps to execute in order to setup the workflow container.
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "default_release_branch": default_release_branch,
        }
        if antitamper is not None:
            self._values["antitamper"] = antitamper
        if artifacts_directory is not None:
            self._values["artifacts_directory"] = artifacts_directory
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if jsii_release_version is not None:
            self._values["jsii_release_version"] = jsii_release_version
        if post_build_steps is not None:
            self._values["post_build_steps"] = post_build_steps
        if prerelease is not None:
            self._values["prerelease"] = prerelease
        if release_branches is not None:
            self._values["release_branches"] = release_branches
        if release_every_commit is not None:
            self._values["release_every_commit"] = release_every_commit
        if release_schedule is not None:
            self._values["release_schedule"] = release_schedule
        if release_workflow_setup_steps is not None:
            self._values["release_workflow_setup_steps"] = release_workflow_setup_steps
        if workflow_container_image is not None:
            self._values["workflow_container_image"] = workflow_container_image

    @builtins.property
    def default_release_branch(self) -> builtins.str:
        '''(experimental) The name of the main release branch.

        NOTE: this field is temporarily required as we migrate the default value
        from "master" to "main". Shortly, it will be made optional with "main" as
        the default.

        :default: "main"

        :stability: experimental
        '''
        result = self._values.get("default_release_branch")
        assert result is not None, "Required property 'default_release_branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def antitamper(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks that after build there are no modified files on git.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("antitamper")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def artifacts_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) A directory which will contain artifacts to be published to npm.

        :default: "dist"

        :stability: experimental
        '''
        result = self._values.get("artifacts_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The initial version of the repo.

        The first release will bump over this
        version, so it will be v0.1.1 or v0.2.0 (depending on whether the first
        bump is minor or patch).

        :default: "v0.1.0"

        :stability: experimental
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsii_release_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version requirement of ``jsii-release`` which is used to publish modules to npm.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("jsii_release_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_build_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after build as part of the release workflow.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("post_build_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def prerelease(self) -> typing.Optional[builtins.str]:
        '''(experimental) Bump as a pre-release (e.g. "beta", "alpha", "pre").

        :default: - normal semantic versions

        :stability: experimental
        '''
        result = self._values.get("prerelease")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Branches which trigger a release.

        Default value is based on defaultReleaseBranch.

        :default: [ "main" ]

        :stability: experimental
        '''
        result = self._values.get("release_branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def release_every_commit(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically release new versions every commit to one of branches in ``releaseBranches``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("release_every_commit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_schedule(self) -> typing.Optional[builtins.str]:
        '''(experimental) CRON schedule to trigger new releases.

        :default: - no scheduled releases

        :stability: experimental
        '''
        result = self._values.get("release_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_workflow_setup_steps(
        self,
    ) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) A set of workflow steps to execute in order to setup the workflow container.

        :stability: experimental
        '''
        result = self._values.get("release_workflow_setup_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def workflow_container_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Container image to use for GitHub workflows.

        :default: - default image

        :stability: experimental
        '''
        result = self._values.get("workflow_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.ReleaseOptions",
    jsii_struct_bases=[ReleaseProjectOptions],
    name_mapping={
        "default_release_branch": "defaultReleaseBranch",
        "antitamper": "antitamper",
        "artifacts_directory": "artifactsDirectory",
        "initial_version": "initialVersion",
        "jsii_release_version": "jsiiReleaseVersion",
        "post_build_steps": "postBuildSteps",
        "prerelease": "prerelease",
        "release_branches": "releaseBranches",
        "release_every_commit": "releaseEveryCommit",
        "release_schedule": "releaseSchedule",
        "release_workflow_setup_steps": "releaseWorkflowSetupSteps",
        "workflow_container_image": "workflowContainerImage",
        "task": "task",
        "version_json": "versionJson",
    },
)
class ReleaseOptions(ReleaseProjectOptions):
    def __init__(
        self,
        *,
        default_release_branch: builtins.str,
        antitamper: typing.Optional[builtins.bool] = None,
        artifacts_directory: typing.Optional[builtins.str] = None,
        initial_version: typing.Optional[builtins.str] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        post_build_steps: typing.Optional[typing.Sequence[_JobStep_c3287c05]] = None,
        prerelease: typing.Optional[builtins.str] = None,
        release_branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        release_every_commit: typing.Optional[builtins.bool] = None,
        release_schedule: typing.Optional[builtins.str] = None,
        release_workflow_setup_steps: typing.Optional[typing.Sequence[_JobStep_c3287c05]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        task: _Task_fb843092,
        version_json: builtins.str,
    ) -> None:
        '''
        :param default_release_branch: (experimental) The name of the main release branch. NOTE: this field is temporarily required as we migrate the default value from "master" to "main". Shortly, it will be made optional with "main" as the default. Default: "main"
        :param antitamper: (experimental) Checks that after build there are no modified files on git. Default: true
        :param artifacts_directory: (experimental) A directory which will contain artifacts to be published to npm. Default: "dist"
        :param initial_version: (experimental) The initial version of the repo. The first release will bump over this version, so it will be v0.1.1 or v0.2.0 (depending on whether the first bump is minor or patch). Default: "v0.1.0"
        :param jsii_release_version: (experimental) Version requirement of ``jsii-release`` which is used to publish modules to npm. Default: "latest"
        :param post_build_steps: (experimental) Steps to execute after build as part of the release workflow. Default: []
        :param prerelease: (experimental) Bump as a pre-release (e.g. "beta", "alpha", "pre"). Default: - normal semantic versions
        :param release_branches: (experimental) Branches which trigger a release. Default value is based on defaultReleaseBranch. Default: [ "main" ]
        :param release_every_commit: (experimental) Automatically release new versions every commit to one of branches in ``releaseBranches``. Default: true
        :param release_schedule: (experimental) CRON schedule to trigger new releases. Default: - no scheduled releases
        :param release_workflow_setup_steps: (experimental) A set of workflow steps to execute in order to setup the workflow container.
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param task: (experimental) The task to execute in order to create the release artifacts. Artifacts are expected to reside under ``artifactsDirectory`` (defaults to ``dist/``) once build is complete.
        :param version_json: (experimental) A name of a .json file to set the ``version`` field in after a bump.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "default_release_branch": default_release_branch,
            "task": task,
            "version_json": version_json,
        }
        if antitamper is not None:
            self._values["antitamper"] = antitamper
        if artifacts_directory is not None:
            self._values["artifacts_directory"] = artifacts_directory
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if jsii_release_version is not None:
            self._values["jsii_release_version"] = jsii_release_version
        if post_build_steps is not None:
            self._values["post_build_steps"] = post_build_steps
        if prerelease is not None:
            self._values["prerelease"] = prerelease
        if release_branches is not None:
            self._values["release_branches"] = release_branches
        if release_every_commit is not None:
            self._values["release_every_commit"] = release_every_commit
        if release_schedule is not None:
            self._values["release_schedule"] = release_schedule
        if release_workflow_setup_steps is not None:
            self._values["release_workflow_setup_steps"] = release_workflow_setup_steps
        if workflow_container_image is not None:
            self._values["workflow_container_image"] = workflow_container_image

    @builtins.property
    def default_release_branch(self) -> builtins.str:
        '''(experimental) The name of the main release branch.

        NOTE: this field is temporarily required as we migrate the default value
        from "master" to "main". Shortly, it will be made optional with "main" as
        the default.

        :default: "main"

        :stability: experimental
        '''
        result = self._values.get("default_release_branch")
        assert result is not None, "Required property 'default_release_branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def antitamper(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks that after build there are no modified files on git.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("antitamper")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def artifacts_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) A directory which will contain artifacts to be published to npm.

        :default: "dist"

        :stability: experimental
        '''
        result = self._values.get("artifacts_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The initial version of the repo.

        The first release will bump over this
        version, so it will be v0.1.1 or v0.2.0 (depending on whether the first
        bump is minor or patch).

        :default: "v0.1.0"

        :stability: experimental
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsii_release_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version requirement of ``jsii-release`` which is used to publish modules to npm.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("jsii_release_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_build_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after build as part of the release workflow.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("post_build_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def prerelease(self) -> typing.Optional[builtins.str]:
        '''(experimental) Bump as a pre-release (e.g. "beta", "alpha", "pre").

        :default: - normal semantic versions

        :stability: experimental
        '''
        result = self._values.get("prerelease")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Branches which trigger a release.

        Default value is based on defaultReleaseBranch.

        :default: [ "main" ]

        :stability: experimental
        '''
        result = self._values.get("release_branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def release_every_commit(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically release new versions every commit to one of branches in ``releaseBranches``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("release_every_commit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_schedule(self) -> typing.Optional[builtins.str]:
        '''(experimental) CRON schedule to trigger new releases.

        :default: - no scheduled releases

        :stability: experimental
        '''
        result = self._values.get("release_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_workflow_setup_steps(
        self,
    ) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) A set of workflow steps to execute in order to setup the workflow container.

        :stability: experimental
        '''
        result = self._values.get("release_workflow_setup_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def workflow_container_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Container image to use for GitHub workflows.

        :default: - default image

        :stability: experimental
        '''
        result = self._values.get("workflow_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def task(self) -> _Task_fb843092:
        '''(experimental) The task to execute in order to create the release artifacts.

        Artifacts are
        expected to reside under ``artifactsDirectory`` (defaults to ``dist/``) once
        build is complete.

        :stability: experimental
        '''
        result = self._values.get("task")
        assert result is not None, "Required property 'task' is missing"
        return typing.cast(_Task_fb843092, result)

    @builtins.property
    def version_json(self) -> builtins.str:
        '''(experimental) A name of a .json file to set the ``version`` field in after a bump.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "package.json"
        '''
        result = self._values.get("version_json")
        assert result is not None, "Required property 'version_json' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Release",
    "ReleaseOptions",
    "ReleaseProjectOptions",
]

publication.publish()

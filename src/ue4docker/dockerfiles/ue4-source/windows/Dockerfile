# escape=`
{% if combine %}
FROM prerequisites as source
{% else %}
ARG NAMESPACE
ARG PREREQS_TAG
FROM ${NAMESPACE}/ue4-build-prerequisites:${PREREQS_TAG}
{% endif %}

{% if not disable_all_patches %}
# Enable verbose output for steps that patch files?
ARG VERBOSE_OUTPUT=0
{% endif %}

{% if source_mode == "copy" %}

# Copy the Unreal Engine source code from the host system
ARG SOURCE_LOCATION
COPY ${SOURCE_LOCATION} C:\UnrealEngine

{% else %}

# The git repository that we will clone
ARG GIT_REPO=""

# The git branch/tag/commit that we will checkout
ARG GIT_BRANCH=""

# Retrieve the address for the host that will supply git credentials
ARG HOST_ADDRESS_ARG=""
ENV HOST_ADDRESS=${HOST_ADDRESS_ARG}

# Retrieve the security token for communicating with the credential supplier
ARG HOST_TOKEN_ARG=""
ENV HOST_TOKEN=${HOST_TOKEN_ARG}

# Install our git credential helper that forwards requests to the host
COPY git-credential-helper.bat C:\git-credential-helper.bat
ENV GIT_ASKPASS=C:\git-credential-helper.bat
# See https://github.com/git-ecosystem/git-credential-manager/blob/main/docs/environment.md#GCM_INTERACTIVE
ENV GCM_INTERACTIVE=false

# Clone the UE4 git repository using the host-supplied credentials
WORKDIR C:\
RUN mkdir C:\UnrealEngine && `
	cd C:\UnrealEngine && `
	git init && `
	{% if git_config %}
	{% for key, value in git_config.items() %}
	git config {{ key }} {{ value }} && `
	{% endfor %}
	{% endif %}
	git remote add origin %GIT_REPO% && `
	git fetch --progress --depth 1 origin %GIT_BRANCH% && `
	git checkout FETCH_HEAD

{% endif %}

{% if (not disable_all_patches) and (not disable_windows_setup_patch) %}
# Since the UE4 prerequisites installer appears to break when newer versions
# of the VC++ runtime are present, patch out the prereqs call in Setup.bat
COPY patch-setup-win.py C:\patch-setup-win.py
RUN python C:\patch-setup-win.py C:\UnrealEngine\Setup.bat %VERBOSE_OUTPUT%
{% endif %}

{% if (not disable_all_patches) and (not disable_release_patches) %}
# Apply our bugfix patches to broken Engine releases such as 4.25.4
# (Make sure we do this before the post-clone setup steps are run)
COPY patch-broken-releases.py C:\patch-broken-releases.py
RUN python C:\patch-broken-releases.py C:\UnrealEngine %VERBOSE_OUTPUT%
{% endif %}

# Run post-clone setup steps
# (Note that the `-no-cache` flag disables caching of dependency data in `.git/ue4-gitdeps`, saving disk space)
WORKDIR C:\UnrealEngine
RUN Setup.bat -no-cache {{ gitdependencies_args }}

{% if (not disable_all_patches) and (not disable_example_platform_cleanup) %}
# Remove the sample `XXX` example platform code, since this breaks builds from 4.24.0 onwards
# (For details of what this is, see: <https://forums.unrealengine.com/unreal-engine/announcements-and-releases/1617783-attention-platform-changes-ahead>)
RUN rmdir /s /q C:\UnrealEngine\Engine\Platforms\XXX 2>NUL || exit 0
{% endif %}

{% if (not disable_all_patches) and (not disable_ubt_patches) %}
# Apply our bugfix patches to UnrealBuildTool (UBT)
COPY patch-ubt.py C:\patch-ubt.py
RUN python C:\patch-ubt.py C:\UnrealEngine\Engine\Source\Programs\UnrealBuildTool
{% endif %}

COPY UpdateSentryDsn.ps1 C:\UpdateSentryDsn.ps1
RUN powershell -f C:\UpdateSentryDsn.ps1 "https://o1258984.ingest.sentry.io/api/6433709/unreal/ff3e17918d764793a3d16beafb39c19a/"

COPY patch-asan.py C:\patch-asan.py
RUN python C:\patch-asan.py C:\UnrealEngine\Engine\Source\Programs\AutomationTool

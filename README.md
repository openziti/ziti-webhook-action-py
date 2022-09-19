# ziti-webhook-action-py
GitHub Action that sends a GitHub webhook over OpenZiti with Python

This GitHub workflow action uses [Ziti Python SDK](https://github.com/openziti/ziti-sdk-py) to post the GitHub event's payload information to a private server over a `Ziti` connection.

## Usage

See [action.yml](action.yml) for descriptions of all available inputs.

```yml
name: ziti-webhook-action-py
on:
  create:
  delete:
  issues:
  issue_comment:
  pull_request_review:
  pull_request_review_comment:
  pull_request:
  push:
  fork:
  release:
    types: [released]

jobs:
  ziti-webhook:
    runs-on: ubuntu-latest
    name: Ziti Webhook Job
    steps:
    - uses: openziti/ziti-webhook-action-py@v1
      with:
        # Identity JSON containing key to access a Ziti network
        zitiId: ${{ secrets.ZITI_WEBHOOK_IDENTITY }}

        # URL to post the payload. Note that the `zitiId` must provide access to a service 
        # intercepting `my-webhook-ziti-server`
        webhookUrl: https://{my-webhook-server}/plugins/github/webhook

        eventJson: ${{ toJson(github.event) }}
```

### Inputs

#### `zitiId`

The `zitiId` input is the JSON formatted string of an identity enrolled  in an OpenZiti Network.

The identity can be created by enrolled via the `ziti edge enroll path/to/jwt [flags]` command.  The `ziti` CLI executable can be obtained [here](https://github.com/openziti/ziti/releases/latest) or you may run the CLI with Docker.

```bash
# produces identity config file ./github.json
docker run --rm --volume ${PWD}:/mnt/ openziti/quickstart /openziti/ziti-bin/ziti edge enroll /mnt/github.jwt 
```

#### `webhookUrl`

This input value is an incoming webhook URL that you have published with OpenZiti to the identity specified by `zitiId`.

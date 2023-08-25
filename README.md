# new-cloud-skeleton

*ℹ️ NOTE: This guide will change as SkyPilot develops. Please check back often to make sure you have the most up-to-date version. The read me in this doc has been derived from the [Google Doc](https://docs.google.com/document/d/1iuPyQ47HloKuHfOYjcRNz7HAlUxFHs2WjMqedYmcPVQ/edit#heading=h.nby65cfuzxoq)*

Skeleton repo for what's needed to add a new cloud.

Detailed instructions upcoming! Contact the dev team on [SkyPilot Slack](https://slack.skypilot.co/) to get access.

## Introduction to SkyPilot

[SkyPilot](https://github.com/skypilot-org/skypilot) is an intercloud broker -- a framework for running workloads on any cloud. Here are some useful links to learn more:

1. [Introductory Blogpost](https://medium.com/@zongheng_yang/skypilot-ml-and-data-science-on-any-cloud-with-massive-cost-savings-244189cc7c0f) [Start here if you are new]
2. [Documentation](https://skypilot.readthedocs.io/en/latest/)
3. [The Sky Above the Clouds](https://arxiv.org/abs/2205.07147)
4. [GitHub](https://github.com/skypilot-org/skypilot)

## How does SkyPilot work?

Here's a simplified overview of SkyPilot's architecture.

In this diagram, the user has two clouds enabled (AWS and GCP). This is what happens when a user launches a job with sky launch:

1. The optimizer reads AWS Catalog and GCP Catalog and runs an algorithm to decide which cloud to run the job on. (Let's suppose the optimizer chooses AWS.) This information is then sent to the provisioner+executor.
   - A catalog is a list of instance types and their prices.
2. The provisioner+executor executes ray commands to launch a cluster on AWS.
   - AWS Node Provider is the interface between ray and AWS, translating ray function calls to AWS API calls.
3. Once the cluster is launched, the provisioner+executor ssh’s into the cluster to execute some AWS Setup commands. This is used to download some important packages on the cluster.
4. The provisioner+executor submits the job to the cluster and the cluster runs the job.

When all is done, the user can run sky down and provisioner+executor will tear down the cluster by executing more ray commands.

## Getting Started

SkyPilot currently supports five possible clouds (AWS, GCP, Azure, RunPod, and Lambda Cloud). Now let's say you have a new cloud, called FluffyCloud, that you want SkyPilot to support. What do you need to do?

You need to:

1. Write a NodeProvider for FluffyCloud. This is the most important part.
2. Add the FluffyCloud catalog to SkyPilot and write functions that read this catalog.
3. Write FluffyCloud setup code.
4. Add FluffyCloud credential check to verify locally stored credentials. This is needed for a user to enable FluffyCloud.

For reference, here is an actual merged PR for adding a new cloud to help you estimate what is required:

- [Lambda Cloud](https://github.com/skypilot-org/skypilot/pull/1557)

By completing the following steps, you will be able to run SkyPilot on FluffyCloud.

- [Step 0](/docs/integration_steps/step_0-api-library.md)
- [Step 1](/docs/integration_steps/step_1-node-provider.md)
- [Step 2](/docs/integration_steps/step_2-catalog.md)
- [Step 3](/docs/integration_steps/step_3-setup-code.md)
- [Step 4](/docs/integration_steps/step_4-setup-code.md.md)
- [Step 5](/docs/integration_steps/step_5-e2e-failover.md)

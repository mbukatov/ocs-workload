Simple testing workloads for OCS 4.

## Usage

To run a workload, create new project (k8s namespace), and run `oc
create` on particular workload file there, eg.:

```
$ oc new-project test-cephfs
$ oc create -f workload_storageutilization_cephfs.yaml
persistentvolumeclaim/fio-target created
configmap/fio-config created
job.batch/fio created
```

When the workload ends with success, you will see the fio job with single
completion, and it's pod in `Completed` state:

```
$ oc get all
NAME            READY   STATUS      RESTARTS   AGE
pod/fio-vvdbl   0/1     Completed   0          4m34s

NAME            COMPLETIONS   DURATION   AGE
job.batch/fio   1/1           18s        4m35s
```

Use `oc logs` to fetch output from `fio` process:

```
$ oc logs job/fio | head
{
  "fio version" : "fio-3.18",
  "timestamp" : 1617125796,
  "timestamp_ms" : 1617125796653,
  "time" : "Tue Mar 30 17:36:36 2021",
  "jobs" : [
    {
      "jobname" : "simple-write",
      "groupid" : 0,
      "error" : 0
```

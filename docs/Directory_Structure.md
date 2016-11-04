# Directory structure

There are quite a few files associated with each subject. Some of them,
like those in 'model' are generated via FSL.  There is raw data in 'BOLD'
and 'anatomy'.  There are also experiment specific files such as
'task_order.txt' and other files in 'model'.

Subject directory:

```
data
+--subNNN
|  +--BOLD
|     +--tasknnn_runNNN
|        +--QA
|        +--bold.nii.gz
|        +--bold_mcf.nii.gz
|        +--
|        +--
|        +--
|     +--tasknnn_runNNN
|     +--tasknnn_runNNN
|  +--anatomy
|     +--highresNNN.nii.gz
|     +--highresNNN_brain.nii.gz
|     +--highresNNN_brain_mask.nii.gz
|     +--t1_NNN_defaced.nii.gz
|     +--t1_nnn_defaced.nii.gz
|     +--t2_NNN_defaced.nii.gz
|  +--behav
|  +--model
|  +--task_order.txt
```

Metadata directory:
```
data
+--ds115_metadata
```


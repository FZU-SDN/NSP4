# NSP4: Network Simulator for P4

**NSP4 is still under developing so that many functions are not supported in NSP4 yet. We invite you to extend NSP4 to create a better environment of learning P4 language.**

## Experiment Preparation

1、In the directory of **src**，change the path information from ```/home/wpq``` to the NSP4 directory information. The code need to modify contain the following file:

-  show_sw_tables.py
-  show_table_entry.py
-  show_table_info.py
-  table_add_entry.py
-  table_delete_entry.py

Example, for the ```show_sw_tables.py```, you should change the sentence from 

```
cmd = "python /home/wpq/NSP4/src/simple_switch_CLI --thrift-port %d < /home/wpq/NSP4/src/cmd/show_tables.txt" % thrift_port
```

to

```
cmd = "python <path for NSP4>/src/simple_switch_CLI --thrift-port %d < /home/wpq/NSP4/src/cmd/show_tables.txt" % thrift_port
```

2、In the directory of **p4web**, change some path information in the code of the file ```p4web.py```.

Like 1, you just modify the information from ```/home/wpq``` to the NSP4 directory, the line number of code includes 70、77、94、118、162、177、201.

## Hands-on Steps

1、Put the P4 code which is correct to the directory of **p4src**.

2、Start up the ```p4web.py``` by the Ryu command **ryu-manager**.

```
ryu-manager ./p4web.py
```

3、Type 127.0.0.1:8080 on your browser，you will see the following interface.

![1](http://images2015.cnblogs.com/blog/990007/201705/990007-20170531124619618-154243598.png)

4、Input the information of topology on the interface, and click the button of **提交**, you will find the GUI of topology appear the browser. Then start up the mininet with P4 by the following command.

![2](http://images2015.cnblogs.com/blog/990007/201705/990007-20170531124620539-1327136931.png)

![3](http://images2015.cnblogs.com/blog/990007/201705/990007-20170531124623196-1485318798.png)

```
cd init
sudo ./run_demo.sh
```

5、Then you can choose the switch by the switch number to config the P4 switch table.

For example:

 5-1、Choose S1

![4](http://images2015.cnblogs.com/blog/990007/201705/990007-20170531124630274-1078869477.png)

 5-2、Add flow entry to the table of **dmac**

![5](http://images2015.cnblogs.com/blog/990007/201705/990007-20170531124632274-709174381.png)

![6](http://images2015.cnblogs.com/blog/990007/201705/990007-20170531124633461-1679913531.png)

 5-3、Then you can fine the flow entry just downloaded appear the interface

![7](http://images2015.cnblogs.com/blog/990007/201705/990007-20170531124634618-1109635584.png)

 5-4、Delete the flow entry

![8](http://images2015.cnblogs.com/blog/990007/201705/990007-20170531124637539-179970778.png)

## Existing Problems

- The path information is complex
- Some function  such as counter is not supported
- Non-support of P4-16 language

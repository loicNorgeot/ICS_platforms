#MeSU statistics

Processing.js script to visualize the usage of MeSU servers on a given time interval, classified by Laboratory or by User.

![MeSU stats](https://cloud.githubusercontent.com/assets/11873158/12446458/5aac795a-bf6a-11e5-9c2a-1f3b00d9cc8e.png "Statistiques d'utilisation")

## PBS data generation

The python script pbsacctsql.py has to be ran regularly on MeSU servers, as it
will export a .csv file (similar to pbsacctsql.csv) used as input in the
Processing.js script.
The pbsacctsql.txt file presents an output of the pbsacctsql command ran on
MeSU servers.

## Processing.js script

HTML code:
```
<script src="/fileadmin/user_upload/PROCESSING/processing.js"></script>
<!--[if lt IE 9]>
<script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->

<div id="stats" class="overlay">
  <div class="pop-up Sketch">
    <h5>Statistiques d'utilisation</h5>
    <a class="close" href="#">×</a>
    <div class="content">
      <canvas id="SKETCH"
      data-processing-sources="/fileadmin/user_upload/PROCESSING/A_VARIABLES.pde
      /fileadmin/user_upload/PROCESSING/B_functions.pde
      /fileadmin/user_upload/PROCESSING/C_RING.pde
      /fileadmin/user_upload/PROCESSING/C_VEC2.pde
      /fileadmin/user_upload/PROCESSING/C_LABO.pde
      /fileadmin/user_upload/PROCESSING/C_LINE.pde
      /fileadmin/user_upload/PROCESSING/C_USER.pde
      /fileadmin/user_upload/PROCESSING/D_CONTROLS.pde
      /fileadmin/user_upload/PROCESSING/graph.pde"
      style="width:1100px;height:500px">
        <p> Votre navigateur ne prend pas en charge ce plugin. </p>
      </canvas>
    </div>
  </div>
</div>
```

Include in a link:
```
<a href=#stats>Click here to view the stats</a>
```

##Improvements
* Link to a file located on MeSU servers, regularly updated (once every day or so).
* Create tabs: last week, last month, last year.

//GLOBAL VARIABLES

String csv = "http://mesu-smn.dsi.upmc.fr/data/5_year_users.csv";
String legend = "last 365 days data";
int availableHours = 1000*24*270+2000*24*30;

labo[] LABOS;
row[]  LINES;
user[] SORTEDUSERS;
labo[] SORTEDLABS;

int             period     = 1;
int             totalHours = 0;
int             maxHours   = 0;
int             maxUsers   = 0;

float           initTime   = 0;
float           friction   = 0.1;
float           repulsion;//  = 1000;
float           attraction;//= 20;
float           pi         = 3.14;

int             laboRadius = width/2;
int             userRadius = 20;

int             nbUsers    = 10;
int             nbLabos    = 15;

float           angleOffset;

boolean         sortByLab    = true;
boolean         displayUsers = true;
boolean         displayGUI   = true;
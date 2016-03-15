//GLOBAL VARIABLES

String csv = "http://mesu-smn.dsi.upmc.fr/data/5_year_users_shuffled.csv";
int             availableHours = 1000*24*300+2000*24*60;

labo[] LABOS;
row[]  LINES;
user[] SORTEDUSERS;
labo[] SORTEDLABS;

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

int             nbUsers    = 125;
int             nbLabos    = 15;

float           angleOffset;

boolean         sortByLab    = true;
boolean         displayUsers = true;
boolean         displayGUI   = true;
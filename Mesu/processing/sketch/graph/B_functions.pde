
//GENERAL FUNCTIONS

void readFile(String file){
  String[] table = loadStrings(file);
  String[] TABLE = new String[0];
  for(int i = 1 ; i < table.length ; i++)
    TABLE = (String[])append(TABLE,table[i]);
  nbUsers = TABLE.length;
  LINES = new row[0];
  for(int i = 0 ; i < nbUsers ; i++){
    String[] l = TABLE[i].split(",");
    if(l.length != 0)
      LINES = (row[])append(LINES, new row(l[0], l[1], int(l[2])));
      //LINES = (row[])append(LINES, new row(l[0], l[1], int(l[4])));
  }
}

void createLabsFromLines(row[] L){
   angleOffset = random(0,2*pi);
  //create labos from file
  LABOS = new labo[0];
  for(row li : L){
    boolean labExists = false;
    for(labo la : LABOS){
      if(la.n.equals(li._labo))
        labExists = true;
    }
    if(!labExists){
      LABOS = (labo[])append(LABOS, new labo(li._labo));
    }
  }
  colorMode(HSB, LABOS.length,1,1,1);
}
/*
void print(ArrayList<labo> L){
  for(labo l : L)
    println(l.n, l.USERS.size(), l.h);
  println(totalHours, maxHours);
}*/

float diameter(int hours){
  float fillRatio  = 0.05;
  int   canvasArea = width * height;
  float filledArea = fillRatio * canvasArea;
  float area       = (1.0*hours/totalHours) * filledArea;
  float diameter   = sqrt(4 * area / pi);
  return 10 + diameter;
}

void initData(){
  totalHours = 0;
  readFile(csv);
  createLabsFromLines(LINES);
  
  for(labo l : LABOS)
    l.init();
    
  for(labo l : LABOS)
    for(user u : l.USERS)
      u.init();
  
  LABOS = (labo[])append(LABOS, new labo());
  
  sortData();
  
  repulsion  = 1000;
  attraction = 20;
  initTime = millis();
}

void sortData(){
  SORTEDUSERS = new user[11];
  SORTEDLABS  = new labo[11];
  for(int i = 0 ; i < 11 ; i++){
    int h = 0;
    int labH = 0;
    for(labo l : LABOS){
      boolean labSorted = false;
      for(labo LA : SORTEDLABS)
          if(LA == l)
            labSorted = true;
      if(l.h >= labH && !labSorted){
          SORTEDLABS[i] = l;
          labH = l.h;
      }
      
      for(user u : l.USERS){
        boolean yetSorted = false;
        for(user US : SORTEDUSERS)
          if(US == u)
            yetSorted = true;
        if(u.h >= h && !yetSorted){
          SORTEDUSERS[i] = u;
          h = u.h;
        }
      }
    }
  }
}

void displayLegend(){
  if(displayGUI){
    textAlign(LEFT);
    int leftMargin = 20;
    int topMargin  = 20;
    int colorWidth = 20;
    int xOffset    = 0;
    if(sortByLab){
      fill(0,0,0,0.5);
      rect(0,0,210,230);
      textAlign(CENTER);
      fill(0,0,1);
      text("Labs", 105, 15);
      textAlign(LEFT);
      for(int i = 1 ; i < min(11, LABOS.length) ; i++){
        xOffset = 0;
        labo l = SORTEDLABS[i];
        fill(l.c); 
        xOffset = leftMargin;
        rect(xOffset, i*topMargin, colorWidth, topMargin-5);
        fill(0,0,1);
        xOffset += colorWidth + leftMargin;
        text(l.n, xOffset , i*topMargin+15);
        xOffset += 80;
        text(str(l.h) + " h", xOffset, i*topMargin+15);
      }
    }
    if(!sortByLab){
      fill(0,0,0,0.5);
      rect(0,0,270,230);
      textAlign(CENTER);
      fill(0,0,1);
      text("Users", 135, 15);
      textAlign(LEFT);
      for(int i = 0 ; i < min(10, SORTEDUSERS.length) ; i++){
        xOffset = 0;
        user u = SORTEDUSERS[i];
        labo l = u.parent;
        fill(l.c); 
        xOffset = leftMargin;
        rect(xOffset, i*topMargin+20, colorWidth, topMargin-5);
        fill(0,0,1);
        xOffset += colorWidth + leftMargin;
        text(l.n, xOffset , i*topMargin+35);
        xOffset += 60;
        text(u.n, xOffset , i*topMargin+35);
        xOffset += 80;
        text(str(u.h) + " h", xOffset, i*topMargin+35);
      }
    }
    fill(0,0,1);
    int commandsOffset = 20;
    int verticalOffset = 20;
    textAlign(RIGHT);
    text("'R' to reset", width - commandsOffset, verticalOffset);
    text("'L' to sort by lab/user", width - commandsOffset, verticalOffset + 20);
    text("'E' to explode", width - commandsOffset, verticalOffset + 40);
    text("'U' to toogle users", width - commandsOffset, verticalOffset + 60);
    text("'I' to toogle interface", width - commandsOffset, verticalOffset + 80);
    text("Drag & drop to move", width - commandsOffset, verticalOffset + 100);
  }
  
  else{
    fill(0,0,1);
    textAlign(LEFT);
    text("press 'I' to toogle interface", 20, 30);
    textAlign(CENTER);
    for(labo l : LABOS)
      text(l.n, l.pos.x, l.pos.y - l.diam/2 - 5);
    textAlign(LEFT);
  }
}

void explode(){
  initTime = millis();
  for(labo l : LABOS)
    if(!l.center)
      l.pos = new VEC2(width/2 + cos(l.angle) * (diameter(maxHours) + 0), height/2 + sin(l.angle) * (diameter(maxHours) + 0));
}

void adjustPhysics(){
  if(mousePressed)
    initTime = millis();
  
  int time = 3000;
  if(millis() - initTime < time && !mousePressed){
    repulsion  = map(millis()-initTime, 0, time, 5000, 1);
    attraction = map(millis()-initTime, 0, time, 500, 0);
    friction   = map(millis() - initTime, 0, time, 0.01, 1);
  }
  if(millis() - initTime > time && !mousePressed)
    noLoop();
    
  if(selected!=null)
    selected.pos = new VEC2(mouseX, mouseY);
}
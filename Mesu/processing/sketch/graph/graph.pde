
//import java.util.Collections;
//import java.util.Comparator;

void setup(){
  size(1000,500);
  initData();
  frameRate(25);
  
  rectMode(CORNER);
  textAlign(CORNER);
  smooth();
}

void draw(){
  background((LABOS.length)/8.);
  for(labo l : LABOS)
    l.compute();
  for(labo l : LABOS)
    l.move();
    
  for(labo l : LABOS){
    l.displayLink();
    for(user u : l.USERS)
      if(displayUsers)
        u.displayLink();
  }
    
  for(labo l : LABOS)
    l.displayBubble();
  for(labo l : LABOS)
    for(user u : l.USERS)
      if(displayUsers)
        u.displayBubble();
  
  displayLegend();
  adjustPhysics();
}

class user{
  String  n;
  int     h;
  labo    parent;
  float   diam;
  float   angle;
  VEC2 pos;
  color   col;
  
  user(labo p, String name, int hours){
    n        = name;
    h        = hours;
    parent   = p;
    maxHours = max(maxHours, h);
  }
  void init(){
    colorMode(HSB, LABOS.length, 1, 1, 1);
    for(int i = 0 ; i < parent.USERS.length ; i++){
      if(parent.USERS[i] == this){
        angle = map(i, 1, maxUsers, parent.angle, parent.angle + 2*pi);
        diam = diameter(h);
      }
    }
    col = color(hue(parent.c) + random(LABOS.length/5.0), 1.0, 1.0, 0.5);//color(hue(parent.c)+random(-LABOS.length/10.,LABOS.length/10.),1.,random(0.5,1),0.5);
  }
  void displayBubble(){
    fill(col);
    noStroke();
    ellipse(pos.x, pos.y, diam, diam);
  }
  void displayLink(){
    stroke(col);
    line(parent.pos.x, parent.pos.y, pos.x, pos.y);
  }
}
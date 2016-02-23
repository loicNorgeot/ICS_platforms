
class labo{
  //Data
  String          n;
  int             h;
  int             maxH = 0;
  user[]          USERS;
  boolean         center = false;
  boolean         selected = false;
  //Vectors
  VEC2         pos;
  VEC2         speed = new VEC2();
  VEC2         accel = new VEC2();
  //Drawing
  color           c;
  float           diam;
  float           angle;
  float           centerAttractionRadius;
  
  labo(String name){
    n     = name;
    createUsers();
    h     = getTotalTime();
  }
  labo(){
    n="";
    USERS = new user[0];
    center = true;
    h = totalHours;
    pos = new VEC2(width/2, height/2);
    c = color(0,0,1,1);
    diam = diameter(totalHours);
  }
  void createUsers(){
    USERS = new user[0];
    for (row l : LINES)
      if (l._labo.equals(n))
        USERS = (user[])append(USERS, new user(this, l._user, l._hours));
    for (user u : USERS)
      maxH = max(maxH, u.h);
  }
  int getTotalTime(){
    int time = 0;
    for(user u : USERS)
      time += u.h;
    totalHours += time;
    return time;
  }
  void init(){
    diam = diameter(h);
    centerAttractionRadius = random(diameter(totalHours), min(width,height)/2);
    //pos = new VEC2(random(width), random(height));
    for(int i = 0 ; i < LABOS.length ; i++){
      if(LABOS[i] == this){
        c     = color(i,0.85,1);
        angle = angleOffset + map(i, 0, LABOS.length, 0, 2*pi);
        float radialOffset = random(diam,width/4);
        pos = new VEC2(width/2 + cos(angle) * (laboRadius+radialOffset), height/2 + sin(angle) * (laboRadius+radialOffset));
      }
    }
    maxUsers = max(maxUsers, USERS.length);
  }
  void displayBubble(){
    if(!center){
      noStroke();
      fill(c);
      ellipse(pos.x, pos.y, diam, diam);
    }
    else{
      ring(width/2, height/2, 0, diam, color(0,0,1));
      arcRing(width/2, height/2, 0, diam, -pi/2, map(totalHours, 0, availableHours, 0, 2) * pi, color(0,0,0.85));
      fill(0,0,0);
      textAlign(CENTER);
      text(str(totalHours) + " h used", width/2, height/2);
      textAlign(LEFT);
    }
  }
  void displayLink(){
    stroke(c);
    line(pos.x, pos.y, width/2, height/2);
  }
  void compute(){
    //Other labs
    boolean neighbour = false;
    for (labo l : LABOS){
      float d      = sqrt(pow(pos.x - l.pos.x,2) + pow(pos.y - l.pos.y,2));
      VEC2 diff = new VEC2(pos.x - l.pos.x, pos.y - l.pos.y);
      //Other labs
      if(l!=this){
        if(d < diam/2 + l.diam/2 + userRadius){
          neighbour = true;
          diff = diff.normalize();
          diff = diff.mult(repulsion/(pow(d,2)));
          accel = diff;//.normalize()
        }
      }
    }
    if(!neighbour)
      accel = new VEC2(0,0);
    speed = speed.sub(new VEC2(friction*speed.x, friction*speed.y));
    
  }  
  void move(){
    VEC2 diff = new VEC2(pos.x - width/2, pos.y - height/2);
    float distToCenter = diff.norm();
    if((distToCenter > diam/2 + centerAttractionRadius))
      accel = accel.add(diff.mult(-attraction/(pow(distToCenter,2))));
    speed = speed.add(accel);
    if(!center)
      pos = pos.add(speed);
    
    //Side constraints
    float m = diam/2 + userRadius;
    //Horizontal constaint
    if(pos.x < m || pos.x > width - m || pos.y < m || pos.y > height - m){
      accel = new VEC2(0,0);
      if(pos.x < m){
        pos.x = m;
        speed.x *= -1;
      }
      else if (pos.x > width - m){
        speed.x *= -1;
        pos.x = width - m;
      }
      //Vertical constraint
      if(pos.y < m){
        speed.y *= -1;
        pos.y = m;
      }
      else if (pos.y > height - m){
        speed.y *= -1;
        pos.y = height - m;
      }
    }
    
    for (user u : USERS)
      u.pos = new VEC2(pos.x + cos(u.angle) * (diam/2 + userRadius), pos.y + sin(u.angle) * (diam/2 + userRadius));
    
    
  }
}

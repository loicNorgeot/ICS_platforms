
void keyPressed(){
  loop();
  if(key=='r')
    initData();
  if(key=='l')
    sortByLab = !sortByLab;
  if(key=='e')
    explode();
  if(key=='u')
    displayUsers = !displayUsers;
  if(key=='i')
    displayGUI = !displayGUI;
}


labo selected;

void mouseReleased(){
  selected = null;
  initTime = millis();//-2000;
  loop();
}
void mouseDragged(){
  initTime = millis();//-2000;
}
void mousePressed(){
  for(labo l : LABOS)
    if(!l.center)
      if(sqrt( pow(mouseX - l.pos.x,2) + pow(mouseY - l.pos.y,2) ) < l.diam/2)
        selected = l;
  initTime = millis();//-2000;
  loop();
  //selected.pos = new VEC2(mouseX, mouseY);
}
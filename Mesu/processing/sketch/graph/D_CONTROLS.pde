
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
  if(key=='x'){
    LABOS = new labo[0];
    LINES = new row[0];
    SORTEDLABS = new labo[0];
    SORTEDUSERS = new user[0];
    period+=1;
    period = period%4;
    if(period==0){
      csv = "http://mesu-smn.dsi.upmc.fr/data/5_total_users_shuffled.csv";
      availableHours = 1;
      legend = "data from service opening";
    }
    if(period==1){
      csv = "http://mesu-smn.dsi.upmc.fr/data/5_year_users_shuffled.csv";
      availableHours = 1000*24*270+2000*24*30;
      legend = "last 365 days data";
    }
    if(period==2){
      csv = "http://mesu-smn.dsi.upmc.fr/data/5_month_users_shuffled.csv";
      availableHours = 1000*24*30+2000*24*30;
      legend = "last month data";
    }
    if(period==3){
      csv = "http://mesu-smn.dsi.upmc.fr/data/5_week_users_shuffled.csv";
      availableHours = 1000*24*7+2000*24*7;
      legend = "last week data";
    }
    initData();
    int t = millis();
    while (millis()-t<200){
      int a = 0;
    }
  }
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
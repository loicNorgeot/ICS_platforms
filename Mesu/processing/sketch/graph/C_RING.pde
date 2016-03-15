void ring(float cX, float cY, float inRad, float outRad, color c){
  arcRing(cX, cY, inRad, outRad, 0, 2*pi, c);
  
}

void arcRing(float cX, float cY, float inRad, float outRad, float start, float end, color c){
  noStroke();
  smooth();
  fill(c);
  arc(cX, cY, outRad, outRad, start, start+end);
  fill(0,0,0);
  ellipse(cX, cY, inRad, inRad);
}

void radialLine(float angle, float cX, float cY, float rad, float length, color c){
  stroke(c);
  line(cX + cos(angle) * rad,
       cY + sin(angle) * rad,
       cX + cos(angle) * (rad + length),
       cY + sin(angle) * (rad + length)
       );
}

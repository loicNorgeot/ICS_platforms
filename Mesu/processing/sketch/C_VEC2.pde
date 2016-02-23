class VEC2{
  float x;
  float y;
  VEC2(){
    x = 0;
    y = 0;
  }
  VEC2(float X, float Y){
    x = X;
    y = Y;
  }
  VEC2(VEC2 v){
    x = v.x;
    y = v.y;
  }
  VEC2 mult(float a){return new VEC2(a*x, a*y);}
  VEC2 add(VEC2 v){  return new VEC2(v.x + x, v.y + y);}
  VEC2 sub(VEC2 v){  return new VEC2(x - v.x, y - v.y);}
  float norm(){      return sqrt(x*x + y*y);}
  VEC2 normalize(){  return this.mult(1./this.norm());}
}
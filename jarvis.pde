import SimpleOpenNI.*;
SimpleOpenNI kinect;

int closestValue;
int closestX;
int closestY;
PrintWriter output;

void setup(){
  size(640, 480);
  kinect = new SimpleOpenNI(this);
  kinect.enableDepth();
  kinect.setMirror(true);
  output = createWriter("coordenadas.txt");
}

void draw(){
  closestValue = 600; 
  kinect.update();
  // get the depth array from the kinect
  int[] depthValues = kinect.depthMap();
  // for each row in the depth image
  for(int y = 0; y < 480; y++){ 
  // look at each pixel in the row
    for(int x = 0; x < 640; x++){
    // pull out the corresponding value from the depth array
    int i = x + y * 640;
    int currentDepthValue = depthValues[i];
// if that pixel is the closest one we've seen so far
    if(currentDepthValue > 0 && currentDepthValue < closestValue){
// save its value
      closestValue = currentDepthValue;
// and save its position (both X and Y coordinates)
      closestX = x;
      closestY = y;
      println(x+","+y);
      output.println(x+","+y);
      output.flush();
      //if(x<320){
          //println("x= "+x + "y= "+y);
      
      //}else{
          //output.println(x+","+y+"\n");
      //}
    }
    }
  }
//draw the depth image on the screen
  image(kinect.depthImage(),0,0);
// draw a red circle over it,positioned at the X and Y coordinates
// we saved of the closest pixel.
  fill(255,0,0);
  ellipse(closestX, closestY, 25, 25);
  
  output.close();
}

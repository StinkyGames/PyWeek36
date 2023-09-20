uniform vec2 u_resolution;

void main(out vec4 fragColor, in vec2 fragCoord){
    vec2 pixelCoord = gl_FragCoord.xy / u_resolution; //Normalized pixel coordinate
    float borderwidth = 0.3;
    vec2 bottomLeft = step(vec2(borderwidth), pixelCoord);
    vec2 topRight = step(vec2(borderwidth), pixelCoord);

    float vec2ToFloat = (bottomLeft.x * bottomLeft.y) * (topRight.x * topRight.y)

    fragColor = vec4(vec3(vec2ToFloat), 1.0);
}
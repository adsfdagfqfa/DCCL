import * as THREE from 'three';
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";



export default class threeInstance {
    constructor(id) {
        this.id = id;
        //绑定的元素
        this.dom = document.getElementById(id);
        //相机
        this.camera2D=null;
        this.camera3D=null;
        this.currentCamera=null;
        //相机初始位置
        this.initialPosition=new THREE.Vector3(300,0,50);
        // 控制器
        this.controls=null;
        //场景
        this.scene=null;
        //渲染器
        this.renderer=null;
        // 创建一个组，用于管理模型
        this.group = new THREE.Group();
        
        // 坐标轴辅助线
        this.axesHelper=null;
        // 环境光
        this.ambientLight=null;  
        // 鼠标位置
        this.mousePosition = new THREE.Vector2();
        // 碰撞检测
        this.raycaster = new THREE.Raycaster();

        // 拖拽模型
        this.dragModel={}
    }
    init() {
        this.initScene();
        this.initCamera();
        this.initRender();
        this.initControls();
        
        this.initaxesHelper();
        this.addLight();
        //窗口改变时场景适配
        window.addEventListener('resize', () => {
            this.currentCamera.aspect = this.dom.offsetWidth / this.dom.offsetHeight;
            this.currentCamera.updateProjectionMatrix();
            this.renderer.setSize(this.dom.offsetWidth, this.dom.offsetHeight);
        });     
    }
    // 创建场景
    initScene() {
        this.scene = new THREE.Scene();
        
    }
    // 创建相机
    initCamera() {
        //相机
        //透视相机,各参数含义,视野角度,宽高比,近端面,远端面
        this.camera3D = new THREE.PerspectiveCamera(75, this.dom.offsetWidth / this.dom.offsetHeight, 0.1, 1000);
        //正交相机,各参数含义,左侧面,右侧面,上侧面,下侧面,近端面,远端面
        this.camera2D = new THREE.OrthographicCamera(this.dom.offsetWidth / -2, 
                                                    this.dom.offsetWidth / 2,  
                                                    this.dom.offsetHeight / 2, 
                                                    this.dom.offsetHeight / -2, 0.1, 1000);
        this.currentCamera=this.camera2D
        // this.currentCamera.position = new THREE.Vector3(this.dom.offsetWidth/2-100,0,10)
        this.currentCamera.position.x=this.dom.offsetWidth/2-100
     
        this.currentCamera.position.z=50
        // this.currentCamera.lookAt(new THREE.Vector3(0,0,0))
        console.log(this.currentCamera.position)

       
    }
    //创建渲染器
    initRender() {
        this.renderer = new THREE.WebGLRenderer({ antialias: true }); //设置抗锯齿
        //设置屏幕像素比
        this.renderer.setPixelRatio(window.devicePixelRatio);
        //渲染的尺寸大小
        this.renderer.setSize(this.dom.offsetWidth, this.dom.offsetHeight);
        // 设置为浅灰色
        this.renderer.setClearColor(0xeeeeee); 
        this.dom.appendChild(this.renderer.domElement);
    }

    //创建控制器
    initControls(){
        this.controls = new OrbitControls(this.currentCamera, this.renderer.domElement);
        //this.controls.target.set(0, 0, 0);
    }
    
    //创建坐标
    initaxesHelper(){
        // 坐标轴辅助线
        this.axesHelper = new THREE.AxesHelper(1000);//100为其长度
        // this.axesHelper.visible = false;
        this.scene.add(this.axesHelper);
    }
    setupScene() {
        // this.addLight();
        // this.addMirrors(-10);
        // this.addLenses(20);
        // this.addGainMedium(30);
    }

    addLight() {
        const ambientLight = new THREE.AmbientLight(0x404040);
        this.scene.add(ambientLight);
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
        directionalLight.position.set(-1, 2, 4).normalize();
        this.scene.add(directionalLight);
    }
    // 切换相机的函数
    switchCamera(cameraType) {
        console.log (cameraType);
        if ( cameraType === '2D' ) {
            this.currentCamera = this.camera2D;
            
            this.resetCameraToNegativeZ()
            console.log(this.currentCamera.position)
            this.controls.object = this.camera2D;
            this.controls.enableRotate = false; // 禁用旋转
            this.controls.enableZoom = true; // 启用缩放
            //将其左键设计为平移
            this.controls.mouseButtons = { LEFT: THREE.MOUSE.PAN, MIDDLE: THREE.MOUSE.DOLLY, RIGHT: THREE.MOUSE.PAN };
        } 
        else if ( cameraType==='3D' ) {
            this.currentCamera = this.camera3D;
            
            this.resetCameraToNegativeZ();
            this.controls.object = this.camera3D;
            this.controls.enableRotate = true; // 启用旋转
            this.controls.enableZoom = true; // 启用缩放
            this.controls.mouseButtons = { LEFT: THREE.MOUSE.ROTATE, MIDDLE: THREE.MOUSE.DOLLY, RIGHT: THREE.MOUSE.PAN };
        }
        //this.controls.update();
    } 
    //重置相机位置，并使其对准Z轴负半轴
    resetCameraToNegativeZ() {
        this.currentCamera.position.set(this.initialPosition.x,this.initialPosition.y,this.initialPosition.z);
        const direction = new THREE.Vector3(0, 0, -1); // Z轴负半轴方向
        this.currentCamera.lookAt(this.initialPosition.clone().add(direction)); // 相机沿指定方向看
    }
    //保存拖拽的模型的相应参数
    setDragModel(model){
        this.dragModel=model
        console.log(this.dragModel)
    }

    // 动画循环
    animate = () => {
        requestAnimationFrame(this.animate);
        if (this.controls.enabled) {
            this.controls.update(); // 更新轨道控制器
        }
        if(this.currentCamera===this.camera2D){
            // console.log(this.currentCamera.position)
            var  direction = new THREE.Vector3(0, 0, -100); // Z轴负半轴方向
            this.currentCamera.lookAt(this.currentCamera.position.clone().add(direction)); // 相机沿指定方向看
        }
        this.renderer.render(this.scene, this.currentCamera);
    }
}


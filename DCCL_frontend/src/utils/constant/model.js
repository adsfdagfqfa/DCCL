const opticalModelList=[
    {
        name: '凸透镜',
        type: 'lens',
        // position: null,
        focalLength: 0.03,
        radius: 0.012
    },
    {
        name: '平面镜',
        type: 'mirror',
        // position :null,
        reflectivity:1,
        radius:0.012,
    },
    {
        name:'介质',
        type:'medium',
        // position:null,
        radius:0.003,
        length:0.001,
        // sigma:15.6e-23,     //Nd:YVO4 吸收发射截面
        // tau:100e-6          //Nd:YVO4 介质上能级粒子寿命
    }
]
const keyMappings={
  radius:"半径(m)",
  length:"长度(m)",
  pumpEfficiency:"泵浦效率",//泵浦效率
  sigma:"受激发射截面(m²)", //Nd:YVO4 吸收发射截面
  tau:"上能级粒子寿命(s)",  //Nd:YVO4 介质上能级粒子寿命
  reflectivity:"反射率",
  focalLength:"焦距(m)",
  speedOfLight: "光速(m/s)",
  planckConstant: "普朗克常量(J·s)",
  vacuumPermittivity: "真空介电常数(F/m)",
  vacuumPermeability: "真空磁导率(H/m)",
  elementaryCharge: "元电荷(C)",
  pumpEfficiency:"泵浦效率",
  pumpWatt:"泵浦功率(W)",
  lambda:"波长(nm)",
  sampleNumber:"采样点数量",
  windowExpandFactor:"窗口扩展因子",
}

const rangeLimits= {
  //元件参数范围
  focalLength: {min: 0, max: 1},
  radius:{min: 0, max: 1},
  length:{min: 0, max: 1},
  reflectivity:{min: 0, max: 1},
  //仿真参数范围
  pumpEfficiency: { min: 0, max: 1 },
  pumpWatt: { min: 0, max: 1000 },
  lambda: { min: 700, max: 2500 }
}
export {opticalModelList , keyMappings , rangeLimits}
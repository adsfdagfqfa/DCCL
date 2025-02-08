const opticalModelList=[
    {
        id: 1,
        name: '凸透镜',
        type: 'lens',
        // position: null,
        focalLength: 0.03,
        radius: 0.012
    },
    {
        id: 2,
        name: '平面镜',
        type: 'mirror',
        // position :null,
        reflectivity:1,
        radius:0.012,
    },
    {
        id: 3,
        name:'介质',
        type:'medium',
        // position:null,
        radius:0.003,
        length:0.001,
        pumpEfficiency:0.72,//泵浦效率
        sigma:15.6e-23,     //Nd:YVO4 吸收发射截面
        tau:100e-6          //Nd:YVO4 介质上能级粒子寿命

    }
]
const keyMappings={
    radius:"半径(m)",
    length:"长度(m)",
    pumpEfficiency:"泵浦效率",//泵浦效率
    sigma:"受激发射截面(m²)", //Nd:YVO4 吸收发射截面
    tau:"上能级粒子寿命(s)",  //Nd:YVO4 介质上能级粒子寿命
    reflectivity:"反射率",
    focalLength:"焦距(m)"
}
export {opticalModelList,keyMappings}
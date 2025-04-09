<template>
    <div>
        <div class="flex gap-4">
            <el-select v-model="yLabel" placeholder="Select Y">
                <el-option v-for="item in yLabels" :key="item" :label="item" :value="item"/>
            </el-select>
            <el-select v-model="xLabel" placeholder="Select X">
                <el-option v-for="item in xLabels" :key="item" :label="item" :value="item"/>
            </el-select>
            <el-button type="primary" @click="drawPlot">生成图表</el-button>
        </div>
        <div ref="plotContainer" class="chart-container"></div>
    </div>
</template>

<script setup>
import { ref,onMounted,getCurrentInstance,onUnmounted } from 'vue';
import { useThreeInstanceStore } from '@/store';
const store=useThreeInstanceStore();
const pageInstance = getCurrentInstance();
const xLabels=ref()
const yLabels=ref(["outputPower"])
const xLabel=ref('')
const yLabel=ref('')
const data=ref([])
//绘图使用的是d3库，在index.html中以CDN形式引入
onMounted(async () => {
    //获取xLabels的数据
    // 一次性解析整个数组
    const parsedData = store.simulationResult.map(item => JSON.parse(item.content));
    console.log(parsedData)
    // const parsedContent = JSON.parse(store.simulationResult[0].content);
    xLabels.value=Object.keys(parsedData[0].selectedAttribute)

    for (const item of parsedData) {
        if(item.isEnd){
            data.value.push({
                x:item.selectedAttribute[xLabel.value],
                y:item[yLabel.value]
            })
        }
    }
    data.value = [
        { x: 0, y: 10 },
        { x: 1, y: 20 },
        { x: 2, y: 30 },
        { x: 3, y: 40 },
        { x: 4, y: 50 },
        { x: 5, y: 60 }
    ];
    console.log('plot','挂载')
});
onUnmounted(() => {
  // 清理资源
  d3.select(pageInstance.refs.plotContainer.value).selectAll('*').remove();
});

function drawPlot(){
    const width = 600;
    const height = 400;
    console.log("plot","绘图")
    console.log(pageInstance.refs.plotContainer)
    // 创建 SVG 元素
    const svg = d3.select(pageInstance.refs.plotContainer)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // 设置坐标轴范围
    const xScale = d3.scaleLinear()
        .domain([0, data.value.length-1])
        .range([50, width - 50]);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(data.value,d=>d.y)])
        .range([height - 50, 50]);

    // 创建折线生成器
    const line = d3.line()
        .x(d => xScale(d.x))
        .y(d => yScale(d.y));

    // 绘制折线
    svg.append('path')
        .datum(data.value)
        .attr('fill', 'none')
        .attr('stroke', 'steelblue')
        .attr('stroke-width', 2)
        .attr('d', line);

    // 添加 X 轴
    svg.append('g')
        .attr('transform', `translate(0,${height - 50})`)
        .call(d3.axisBottom(xScale));

    // 添加 Y 轴
    svg.append('g')
        .attr('transform', `translate(50,0)`)
        .call(d3.axisLeft(yScale));
}
</script>

<template>
  <div class="card">
    <el-image :src="imgPath" style="width: 100%; height: 200px;">

    </el-image>
    <div class="cardHeader">
      <h2>{{ title }}</h2>
    </div>
    <div class="card-body">
      <p>{{ description }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    imgPath: String,
    title: String,
    description: String,
  }
}
</script>

<style scoped>
.card {
  width: 400px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  transition: transform 0.3s ease-in-out;
}

.card:hover {
  transform: translateY(-5px);
}

.cardHeader {
  color: #000000;
  padding: 20px;
  font-size: 24px;
}

.card-body {
  padding: 20px;
  background: white;
  font-size: 16px;
}

h2 {
  margin: 0;
  font-size: 24px;
}

p {
  margin: 0;
  color: #666;
}

.el-image {
  max-width: 400px;
  overflow: hidden;
}

.purple {
  background: #8257e6;
}

.blue {
  background: #2196f3;
}

.red {
  background: #f44336;
}

.darkblue {
  background: #3f51b5;
}
</style>

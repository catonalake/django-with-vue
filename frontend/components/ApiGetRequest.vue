<script setup>
import axios from 'axios'
import { ref, reactive, onMounted } from 'vue';

let data = reactive({
    title: "hello hello world",
    contentList: []
})

onMounted(async () =>{
    let response;
    try {
        response = await axios.get('/api/posts/')
    } catch (error) {
        response = error.response
        console.error(response)
    }
    console.log(response)
    if (response.status === 200) {
        console.log(response.data)
        let responseData = response.data
        data.contentList = responseData.data
        data.title = "Post"  + ` "reactive way"` 
    } else {
        data.title = "Not Found"
    }

})

</script>

<template>
    <div>
        <h2>  {{ data.title }} </h2>
        <div v-for="post of data.contentList" :key="post.id">
            {{ post.id }} = {{ post.title }}
        </div>

    </div>
</template>
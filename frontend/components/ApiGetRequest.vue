<script setup>
import { ref, reactive, onMounted } from 'vue';
let title = ref("Hello World")
let contentList = ref([])

let data = reactive({
    subTitle: "hello hello world",
    contentListST: []
})

// fetch('/api/posts/').then(res=>console.log(res))
onMounted(async () =>{
    let responseData = await fetch('/api/posts/').then(res=>{
        if (res.status === 200) {
            return res.json()
        } else {
            return "Not Found"
        }
    })
    if (responseData instanceof String || typeof(responseData) === "string") {
        title.value = responseData  + ` "ref way"` 
        data.subTitle = responseData  + ` "reactive way"` 
    } else {
        title.value = "Post"
        contentList.value = responseData.data
        data.subTitle = "Posting"
        data.contentListST = responseData.data
    }
    console.log(responseData.data)
})

</script>

<template>
    <div>
        <h2> {{ title }}</h2>
        <div v-for="post of contentList" :key="post.id">
            {{ post.id }} = {{ post.title }}
        </div>

        <h2>  {{ data.subTitle }} </h2>
        <div v-for="post of data.contentListST" :key="post.id">
            {{ post.id }} = {{ post.title }}
        </div>

    </div>
</template>
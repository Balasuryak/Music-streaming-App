export default {
    template: `<div>
    <input type="text" placeholder="topic" v-model="resource.topic"/>
    <input type="text" placeholder="description" v-model="resource.description" />
    <input type="text" placeholder="Resource Link" v-model="resource.resource_link" />
    <button @click="createResource"> Create Resource</button>
    </div>`
}
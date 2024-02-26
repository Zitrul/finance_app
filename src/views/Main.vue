<template>
  <div>
    <h1>This is MAAAAAAAin page</h1>
  </div>
  <div class="absolute_forms">
    <Sign></Sign>
  </div>
</template>

<script>
import Sign from '@/components/Sign.vue'
import * as fun from '@/functions.js'

export default {
  name: 'Main',
  components: {
    Sign
  },
  data(){
    return {
    }
  },
  methods: {
  },
  mounted(){
  }
}
</script>
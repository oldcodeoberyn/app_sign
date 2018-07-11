<template>
  <div>
    <v-header class="pos-header"></v-header>
    <v-nav></v-nav>
  </div>
</template>

<script>
import vHeader from '@/components/vHeader'
import vNav from '@/components/vNav'
export default {
  created() {
  },
  components: {
    vHeader,
    vNav
  },
  computed: {
    showMy() {
      return this.$store.state.showMy
    }
  }
}
</script>

<style lang="css" scoped>
.pos-header {
  position: fixed;
  top: 0;
}
</style>

<script>
import { useDisplay } from 'vuetify'

export default {
    name: 'display',
    setup() {
        const { xs, sm, smAndDown, smAndUp, md, mdAndDown, mdAndUp, lg, lgAndDown, lgAndUp, xl, xlAndDown, xlAndUp, xxl } = useDisplay();
        return {
            xs,
            sm,
            smAndDown,
            smAndUp,
            md,
            mdAndDown,
            mdAndUp,
            lg,
            lgAndDown,
            lgAndUp,
            xl,
            xlAndDown,
            xlAndUp,
            xxl
        }
    }
}
</script>
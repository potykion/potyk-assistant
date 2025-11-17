import {defineContentConfig, defineCollection} from '@nuxt/content'
import {z} from 'zod'

export default defineContentConfig({
    collections: {
        content: defineCollection({
            type: 'page',
            source: '**/*.md',

            // https://content.nuxt.com/docs/collections/define#collection-schema
            schema: z.object({
                date: z.date(),
                tags: z.array(z.string()),

            })
        })
    }
})

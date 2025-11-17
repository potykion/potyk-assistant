// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: {enabled: true},
    modules: ['@nuxt/content', '@nuxt/fonts', 'vuetify-nuxt-module', '@nuxt/eslint'],
    ssr: true,
    content: {
        renderer: {
            anchorLinks: {h2: false, h3: false, h4: false},
        },
    },
    // when enabling ssr option you need to disable inlineStyles and maybe devLogs
    features: {
        inlineStyles: false,
        devLogs: false,
    },

    build: {
        transpile: ['vuetify'],
    },

    vite: {
        ssr: {
            noExternal: ['vuetify'],
        },
    },

    css: ['~/assets/global.scss'],

    vuetify: {
        moduleOptions: {
            // check https://nuxt.vuetifyjs.com/guide/server-side-rendering.html
            ssrClientHints: {
                reloadOnFirstRequest: false,
                viewportSize: true,
                prefersColorScheme: false,

                prefersColorSchemeOptions: {
                    useBrowserThemeOnly: false,
                },
            },

            // /* If customizing sass global variables ($utilities, $reset, $color-pack, $body-font-family, etc) */
            // disableVuetifyStyles: true,
            styles: {
                configFile: 'assets/settings.scss',
            },
        },
    },
})
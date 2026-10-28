const config = {
  title: 'BUOI6 DevSecOps',
  tagline: 'Pipeline CI/CD an toàn',
  favicon: 'img/favicon.ico',
  url: 'https://duongthanhmong.gitlab.io',
  baseUrl: '/buoi6-docusaurus-pipeline/',
  organizationName: 'duongthanhmong',
  projectName: 'buoi6-docusaurus-pipeline',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  i18n: {
    defaultLocale: 'vi',
    locales: ['vi']
  },
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.js'
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css'
        }
      }
    ]
  ]
};

module.exports = config;

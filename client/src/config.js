// import runtimeEnv from '@mars/heroku-js-runtime-env';

// const env = runtimeEnv()
const config = {
  apiBasePath: process.env.REACT_APP_API_BASE_PATH,
  reactAppMode: process.env.REACT_APP_MODE,
}

export default config

// import axios from "axios";

// /*
//   ⚠️ بدل IP تحت ب IP ديال PC لي فيه backend
//   مثال:
//   Windows → ipconfig
//   Mac → ifconfig
// */

// const API = axios.create({
//   baseURL: "http://192.168.1.15:8080/api", // 🔴 بدلها ب IP ديالك
//   timeout: 10000,
//   headers: {
//     "Content-Type": "application/json",
//   },
// });

// /*
//   🔐 Automatically attach JWT token
//   كيضيف Authorization header فكل request
// */
// API.interceptors.request.use(
//   (config) => {
//     const token = global.jwtToken;

//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`;
//     }

//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );

// /*
//   ❌ Handle 401 (token expired)
// */
// API.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     if (error.response && error.response.status === 401) {
//       console.log("Unauthorized - Token expired");
//       // تقدر هنا تدير logout أو redirect
//     }

//     return Promise.reject(error);
//   }
// );

// export default API;

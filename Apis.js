import axios from "axios";

export const BASE_URL = "http://192.168.1.13:8000";

// export const endpoints = {
//   login: "/api/login/",
//   register: "/api/register/",
//   currentUser: "/api/users/me/",

//   services: (page = 1) => `/api/services/?page=${page}&page_size=20`,
//   serviceDetails: (id) => `/api/services/${id}/`,
//   bookings: "/api/bookings/",
//   payments: "/api/payments/",
//   // reviews: (serviceId) => `/api/reviews/?service_id=${serviceId}`,
//   reviews: "/api/reviews"
// };

export const endpoints = {
  login: "/api/login/",
  register: "/api/register/",
  currentUser: "/api/users/me/",

  services: (page = 1) => `/api/services/?page=${page}&page_size=20`,
  serviceDetails: (id) => `/api/services/${id}/`,

  myBookings: "/api/bookings/",   
  payments: "/api/payments/",
  reviews: "/api/reviews/",
};


export const authApis = (token) =>
  axios.create({
    baseURL: BASE_URL,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

export default axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

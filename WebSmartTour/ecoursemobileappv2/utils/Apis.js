import axios from "axios";


const BASE_URL = "http://192.168.1.5:8000"; 

export const endpoints = {

  login: "/o/token/", 
  currentUser: "/api/users/me/", 
  registerCustomer: "/api/users/", 
  
  
  categories: "/api/services/servicetype/", 
  

  services: (type) => type ? `/api/services/?type=${type}` : '/api/services/',
  serviceDetails: (id) => `/api/services/${id}/`,

  bookings: "/api/bookings/",
  

  reviews: (serviceId) => `/api/reviews/?service_id=${serviceId}`,


  providerReport: "/reports/provider/",
  adminReport: "/reports/admin/",
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
});
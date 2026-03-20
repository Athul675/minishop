import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    axios.get("/api/product-service/products")
      .then(res => setProducts(res.data));
  }, []);

  return (
    <div style={{ padding: 40 }}>
      <h1>MiniShop</h1>
      {products.map(p => (
        <div key={p.id}>
          <h3>{p.name}</h3>
          <p>₹ {p.price}</p>
        </div>
      ))}
    </div>
  );
}

export default App;

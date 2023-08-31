import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const port = 1245;

const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);

function reserveStockById(itemId, stock) {
  return redisClient.set(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
  const reservedStock = await getAsync(`item.${itemId}`);
  return parseInt(reservedStock) || 0;
}

app.use(express.json());

app.get('/list_products', (req, res) => {
  res.json(listProducts.map(product => ({
    itemId: product.itemId,
    itemName: product.itemName,
    price: product.price,
    initialAvailableQuantity: product.initialAvailableQuantity,
  })));
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = listProducts.find(p => p.itemId === itemId);

  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }

  const currentReservedStock = await getCurrentReservedStockById(itemId);

  res.json({
    itemId: product.itemId,
    itemName: product.itemName,
    price: product.price,
    initialAvailableQuantity: product.initialAvailableQuantity,
    currentQuantity: product.initialAvailableQuantity - currentReservedStock,
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = listProducts.find(p => p.itemId === itemId);

  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }

  const currentReservedStock = await getCurrentReservedStockById(itemId);

  if (currentReservedStock >= product.initialAvailableQuantity) {
    res.json({ status: 'Not enough stock available', itemId: itemId });
  } else {
    await reserveStockById(itemId, currentReservedStock + 1);
    res.json({ status: 'Reservation confirmed', itemId: itemId });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

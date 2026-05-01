import { MongoClient, Db, ServerApiVersion } from 'mongodb';
import dotenv from 'dotenv';

dotenv.config();

const uri = process.env.MONGODB_URI;
if (!uri) {
  throw new Error('MONGODB_URI not found in environment variables');
}

const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  },
  tls: true,
  tlsAllowInvalidCertificates: false,
});

let db: Db | null = null;

export async function connectDB(): Promise<Db> {
  try {
    if (db) {
      return db;
    }

    await client.connect();
    await client.db('admin').command({ ping: 1 });
    
    const dbName = process.env.MONGODB_DATABASE || 'q_sync_dev';
    db = client.db(dbName);
    
    console.log('✅ Connected to MongoDB Atlas:', dbName);
    
    // Create indexes for better performance
    await db.collection('tasks').createIndex({ taskId: 1 }, { unique: true });
    await db.collection('tasks').createIndex({ createdAt: -1 });
    await db.collection('files').createIndex({ taskId: 1 });
    
    return db;
  } catch (error) {
    console.error('❌ MongoDB connection failed:', error);
    throw error;
  }
}

export async function getDB(): Promise<Db> {
  if (!db) {
    return await connectDB();
  }
  return db;
}

export async function closeDB(): Promise<void> {
  if (client) {
    await client.close();
    db = null;
    console.log('✅ MongoDB connection closed');
  }
}

// Graceful shutdown
process.on('SIGINT', async () => {
  await closeDB();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  await closeDB();
  process.exit(0);
});

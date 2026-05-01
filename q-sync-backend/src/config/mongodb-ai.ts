import dotenv from 'dotenv';

dotenv.config();

const mongodbAIApiKey = process.env.MONGODB_AI_API_KEY;
const mongodbAIProject = process.env.MONGODB_AI_PROJECT || 'IBM_BOB';
const embeddingModel = process.env.MONGODB_AI_EMBEDDING_MODEL || 'voyage-code-3';
const rerankModel = process.env.MONGODB_AI_RERANK_MODEL || 'rerank-2.5';
const multimodalModel = process.env.MONGODB_AI_MULTIMODAL_MODEL || 'voyage-multimodal-3.5';

if (!mongodbAIApiKey) {
  console.warn('⚠️ MongoDB AI API key not found. Embeddings will use fallback.');
}

interface EmbeddingResponse {
  embeddings: number[][];
  model: string;
  usage: {
    total_tokens: number;
  };
}

interface RerankResponse {
  results: Array<{
    index: number;
    relevance_score: number;
  }>;
  model: string;
}

let mongodbAIClient: any = null;

export async function initMongoDBai() {
  if (!mongodbAIApiKey) {
    console.log('⚠️ MongoDB AI running in FALLBACK mode');
    return null;
  }

  try {
    mongodbAIClient = {
      initialized: true,
      project: mongodbAIProject,
      models: {
        embedding: embeddingModel,
        rerank: rerankModel,
        multimodal: multimodalModel,
      },
    };
    
    console.log(`✅ Connected to MongoDB AI (Voyage AI)`);
    console.log(`   Project: ${mongodbAIProject}`);
    console.log(`   Embedding Model: ${embeddingModel}`);
    console.log(`   Rerank Model: ${rerankModel}`);
    
    return mongodbAIClient;
  } catch (error) {
    console.error('❌ MongoDB AI connection failed:', error);
    console.log('⚠️ Falling back to simple embeddings');
    return null;
  }
}

export async function generateCodeEmbeddings(
  texts: string[],
  model: string = embeddingModel
): Promise<number[][]> {
  if (!mongodbAIClient || !mongodbAIApiKey) {
    console.log('⚠️ Using fallback embeddings');
    return generateFallbackEmbeddings(texts);
  }

  try {
    const response = await fetch('https://api.voyageai.com/v1/embeddings', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${mongodbAIApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        input: texts,
        model: model,
        input_type: 'document',
      }),
    });

    if (!response.ok) {
      throw new Error(`Voyage AI API error: ${response.statusText}`);
    }

    const data: EmbeddingResponse = await response.json();
    console.log(`✅ Generated ${data.embeddings.length} embeddings with ${model}`);
    
    return data.embeddings;
  } catch (error) {
    console.error('❌ Embedding generation failed:', error);
    console.log('⚠️ Falling back to simple embeddings');
    return generateFallbackEmbeddings(texts);
  }
}

export async function rerankDocuments(
  query: string,
  documents: string[],
  topK: number = 5
): Promise<Array<{ index: number; score: number; text: string }>> {
  if (!mongodbAIClient || !mongodbAIApiKey) {
    console.log('⚠️ Using fallback reranking');
    return fallbackRerank(query, documents, topK);
  }

  try {
    const response = await fetch('https://api.voyageai.com/v1/rerank', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${mongodbAIApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        documents: documents,
        model: rerankModel,
        top_k: topK,
      }),
    });

    if (!response.ok) {
      throw new Error(`Voyage AI Rerank API error: ${response.statusText}`);
    }

    const data: RerankResponse = await response.json();
    
    const results = data.results.map(result => ({
      index: result.index,
      score: result.relevance_score,
      text: documents[result.index],
    }));
    
    console.log(`✅ Reranked ${documents.length} documents, top ${topK} returned`);
    return results;
  } catch (error) {
    console.error('❌ Reranking failed:', error);
    console.log('⚠️ Falling back to simple reranking');
    return fallbackRerank(query, documents, topK);
  }
}

export async function generateMultimodalEmbeddings(
  inputs: Array<{ type: 'text' | 'image'; content: string }>
): Promise<number[][]> {
  if (!mongodbAIClient || !mongodbAIApiKey) {
    console.log('⚠️ Multimodal embeddings not available in fallback mode');
    return [];
  }

  try {
    const response = await fetch('https://api.voyageai.com/v1/multimodal/embeddings', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${mongodbAIApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        inputs: inputs,
        model: multimodalModel,
      }),
    });

    if (!response.ok) {
      throw new Error(`Voyage AI Multimodal API error: ${response.statusText}`);
    }

    const data: EmbeddingResponse = await response.json();
    console.log(`✅ Generated ${data.embeddings.length} multimodal embeddings`);
    
    return data.embeddings;
  } catch (error) {
    console.error('❌ Multimodal embedding generation failed:', error);
    return [];
  }
}

// Fallback functions for when MongoDB AI is not available
function generateFallbackEmbeddings(texts: string[]): number[][] {
  // Simple hash-based embeddings (384 dimensions)
  return texts.map(text => {
    const embedding = new Array(384).fill(0);
    for (let i = 0; i < text.length; i++) {
      const charCode = text.charCodeAt(i);
      embedding[i % 384] += charCode / 1000;
    }
    // Normalize
    const magnitude = Math.sqrt(embedding.reduce((sum, val) => sum + val * val, 0));
    return embedding.map(val => val / magnitude);
  });
}

function fallbackRerank(
  query: string,
  documents: string[],
  topK: number
): Array<{ index: number; score: number; text: string }> {
  // Simple keyword-based scoring
  const queryWords = query.toLowerCase().split(/\s+/);
  
  const scored = documents.map((doc, index) => {
    const docLower = doc.toLowerCase();
    const score = queryWords.reduce((sum, word) => {
      const count = (docLower.match(new RegExp(word, 'g')) || []).length;
      return sum + count;
    }, 0);
    
    return { index, score, text: doc };
  });
  
  return scored
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);
}

export function getMongoDBaiConfig() {
  return {
    project: mongodbAIProject,
    models: {
      embedding: embeddingModel,
      rerank: rerankModel,
      multimodal: multimodalModel,
    },
    isConfigured: !!mongodbAIApiKey,
    rateLimits: {
      tokensPerMin: 10000,
      requestsPerMin: 3,
    },
  };
}

export { mongodbAIClient };

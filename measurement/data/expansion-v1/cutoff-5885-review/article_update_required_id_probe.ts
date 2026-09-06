import { applyArticleUpdate } from './solution';
const article = { id: 'a', heading: 'Old', body: 'Old', bookmarkCount: 0 };
Object.defineProperty(article, 'id', { value: 'a', enumerable: false });
const result = applyArticleUpdate({ collections: [{ code: 'c', articles: [article] }], readers: [] }, {
  collectionCode: 'c', articleId: 'a', readerId: 'unused', heading: 'New', body: 'New', bookmarkDelta: 0, revision: 'r'
});
if (!result.ok || result.state.collections[0].articles[0].id !== 'a') throw new Error('Article ID lost during text update');

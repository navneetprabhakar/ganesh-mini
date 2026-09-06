import {ManuscriptPublisher, type ManuscriptRecord} from './solution';
const saved = Object.defineProperty({},'title',{value:'saved',enumerable:false}) as ManuscriptRecord;
const publisher = new ManuscriptPublisher({put:async()=> 'token'}, {save:async()=>saved});
publisher.publish({title:'draft'}).then(result => {
  console.log('title',result.title);
  if(result.title !== 'saved') throw new Error('saved title lost');
});

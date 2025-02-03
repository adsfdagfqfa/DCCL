import *  as NewModel from './newModel'
import { onlyKey } from '../utilityFunction';
class ModelFactory {
  static createModel(type) {
    let model;
    switch (type) {
      case 'lens':
        
        break;
      case 'mirror':
        
        break;
      case 'medium':
        model=NewModel.newMedium()
        break;
      default:
        throw new Error(`Unknown model type: ${type}`);
    }
    model.uuid = onlyKey(5);
    model.name=type+'_'+model.uuid;
    return model;
  }
}
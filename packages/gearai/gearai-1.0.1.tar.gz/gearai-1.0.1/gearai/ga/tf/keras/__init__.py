#------------------------------------------------------------------------------------------------

# GEAR AI

# gearai.ga.tf.keras SUBPACKAGE

# DEVELOPED BY: VIGNESHWAR K R 

# CATEGORIES: ARTIFICIAL INTELLIGENCE, TENSORFLOW

#------------------------------------------------------------------------------------------------

# IMPORTING REQUIRED LIBRARIES
import tensorflow as tf
from tensorflow.python.keras.engine import data_adapter

# CLASS FOR CUSTOM TRAIN STEP IN GRADIENT ACCUMULATION
class customTrainStep(tf.keras.Model):

    def __init__(self,no_grads, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.no_grads = tf.constant(no_grads, dtype = tf.int32)
        self.n_acum_step = tf.Variable(0, dtype = tf.int32, trainable = False)
        self.grad_acc = [tf.Variable(tf.zeros_like(v, dtype=tf.float32), trainable=False) for v in self.trainable_variables]

    def train_step(self,data):
        self.n_acum_step.assign_add(1)
    
        x, y = data

        # GRADIENT TAPE
        with tf.GradientTape() as tape:
            y_pred = self(x, training=True)
            loss = self.compiled_loss(y, y_pred, regularization_losses=self.losses)
        
        # CALCULATING THE BATCH GRADIENTS
        gradients = tape.gradient(loss, self.trainable_variables)

        # ACCUMULATING THE BATCH GRADIENTS
        for i in range(len(self.grad_acc)):
            self.grad_acc[i].assign_add(gradients[i])
 
        
        tf.cond(tf.equal(self.n_acum_step, self.no_grads), self.apply_accu_gradients, lambda: None)

        # UPDATING THE METRICS
        self.compiled_metrics.update_state(y, y_pred)
        return {m.name: m.result() for m in self.metrics}

    def apply_accu_gradients(self):

        # APPLYING ACCUMULATED GRADIENTS
        self.optimizer.apply_gradients(zip(self.grad_acc, self.trainable_variables))

        # RESETTING
        self.n_acum_step.assign(0)
        for i in range(len(self.grad_acc)):
            self.grad_acc[i].assign(tf.zeros_like(self.trainable_variables[i], dtype=tf.float32))



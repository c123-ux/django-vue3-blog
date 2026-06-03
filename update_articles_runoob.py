import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_backend.settings')
django.setup()

from apps.articles.models import Article

# 参考菜鸟教程风格更新文章

articles_content = {
    'React 状态管理': """# React 状态管理

## 什么是状态管理

在 React 应用中，**状态管理**是指管理组件之间共享数据的方式。随着应用规模的增长，组件之间的状态共享变得越来越复杂，需要一种系统化的方式来管理状态。

## 为什么需要状态管理

### 问题场景

当应用变得复杂时，组件之间需要共享数据：

```jsx
// 父子组件传递数据
function Parent() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <Child count={count} />
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}

function Child({ count }) {
  return <GrandChild count={count} />;
}

function GrandChild({ count }) {
  return <p>Count: {count}</p>;
}
```

这种**props drilling**方式在多层组件嵌套时会变得非常繁琐。

## React 内置状态管理

### 1. useState

`useState` 是 React 最基础的状态管理 Hook：

```jsx
import { useState } from 'react';

function Counter() {
  // 声明一个状态变量 count，初始值为 0
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>当前计数: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        点击增加
      </button>
      <button onClick={() => setCount(count - 1)}>
        点击减少
      </button>
      <button onClick={() => setCount(0)}>
        重置
      </button>
    </div>
  );
}
```

**特点：**
- 适用于简单的组件内部状态
- 只能在函数组件中使用
- 状态更新是异步的

### 2. useContext

`useContext` 允许跨组件共享状态：

```jsx
import { createContext, useContext } from 'react';

// 创建 Context
const ThemeContext = createContext('light');

// 提供 Context
function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Toolbar />
    </ThemeContext.Provider>
  );
}

// 消费 Context
function Toolbar() {
  const theme = useContext(ThemeContext);
  return (
    <div style={{ background: theme === 'dark' ? '#333' : '#fff' }}>
      <ThemedButton />
    </div>
  );
}

function ThemedButton() {
  const theme = useContext(ThemeContext);
  return (
    <button style={{ 
      background: theme === 'dark' ? '#666' : '#eee',
      color: theme === 'dark' ? '#fff' : '#333'
    }}>
      主题按钮
    </button>
  );
}
```

**特点：**
- 避免 props drilling
- 适用于全局状态共享
- 当 Context 值变化时，所有消费组件都会重新渲染

## 第三方状态管理库

### Redux

**安装：**
```bash
npm install redux react-redux @reduxjs/toolkit
```

**创建 Store：**
```jsx
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './counterSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
  },
});
```

**创建 Slice：**
```jsx
import { createSlice } from '@reduxjs/toolkit';

const counterSlice = createSlice({
  name: 'counter',
  initialState: {
    value: 0,
  },
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action) => {
      state.value += action.payload;
    },
  },
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;
export default counterSlice.reducer;
```

**使用：**
```jsx
import { useSelector, useDispatch } from 'react-redux';
import { increment, decrement } from './counterSlice';

function Counter() {
  const count = useSelector((state) => state.counter.value);
  const dispatch = useDispatch();
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => dispatch(increment())}>+</button>
      <button onClick={() => dispatch(decrement())}>-</button>
    </div>
  );
}
```

### Zustand

**安装：**
```bash
npm install zustand
```

**创建 Store：**
```jsx
import create from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));
```

**使用：**
```jsx
function Counter() {
  const count = useStore((state) => state.count);
  const increment = useStore((state) => state.increment);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
    </div>
  );
}
```

## 选择合适的方案

| 方案 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| useState | 简单组件状态 | 轻量、易用 | 不适合跨组件共享 |
| useContext | 中等规模应用 | 减少 props 传递 | 可能导致不必要渲染 |
| Redux | 大型复杂应用 | 强大、可预测 | 学习曲线较陡 |
| Zustand | 中小型应用 | 轻量、API简洁 | 生态较小 |

## 实践案例：Todo 应用

```jsx
import { useState } from 'react';

function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [inputValue, setInputValue] = useState('');
  
  const addTodo = () => {
    if (inputValue.trim()) {
      setTodos([...todos, { 
        id: Date.now(), 
        text: inputValue, 
        completed: false 
      }]);
      setInputValue('');
    }
  };
  
  const toggleTodo = (id) => {
    setTodos(todos.map(todo => 
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  };
  
  const deleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };
  
  return (
    <div>
      <input 
        type="text" 
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && addTodo()}
        placeholder="添加待办事项"
      />
      <button onClick={addTodo}>添加</button>
      <ul>
        {todos.map(todo => (
          <li key={todo.id}>
            <span 
              style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}
              onClick={() => toggleTodo(todo.id)}
            >
              {todo.text}
            </span>
            <button onClick={() => deleteTodo(todo.id)}>删除</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## 学习资源

- [React 官方文档](https://react.dev/)
- [Redux 官方文档](https://redux.js.org/)
- [Zustand 官方文档](https://docs.pmnd.rs/zustand)
- [菜鸟教程 React 教程](https://www.runoob.com/react/react-tutorial.html)

## 总结

状态管理是 React 开发中的核心概念，选择合适的方案取决于项目规模和复杂度。初学者可以从 `useState` 和 `useContext` 开始，随着项目增长再考虑引入 Redux 或 Zustand。
""",
    
    'Python 装饰器完全指南': """# Python 装饰器完全指南

## 什么是装饰器

**装饰器**是 Python 中一种强大的语法特性，它允许在不修改函数代码的情况下扩展函数功能。

装饰器本质上是一个**高阶函数**，它接受一个函数作为参数，并返回一个新的函数。

## 基本语法

### 简单装饰器

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        # 在函数执行前做些事情
        print("函数执行前")
        # 调用原函数
        result = func(*args, **kwargs)
        # 在函数执行后做些事情
        print("函数执行后")
        return result
    return wrapper

@decorator
def say_hello():
    print("Hello, World!")

# 调用
say_hello()
```

**输出：**
```
函数执行前
Hello, World!
函数执行后
```

### 带参数的装饰器

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    return "Hello!"

# 调用
result = say_hello()
print(result)  # ['Hello!', 'Hello!', 'Hello!']
```

## 装饰器的应用场景

### 1. 日志记录

```python
def log(func):
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        print(f"参数: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"返回值: {result}")
        return result
    return wrapper

@log
def add(a, b):
    return a + b

# 调用
add(3, 5)
```

**输出：**
```
调用函数: add
参数: args=(3, 5), kwargs={}
返回值: 8
```

### 2. 性能计时

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 耗时: {end_time - start_time:.4f}秒")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(2)
    print("函数执行完成")

# 调用
slow_function()
```

### 3. 身份验证

```python
def authenticate(func):
    def wrapper(*args, **kwargs):
        is_logged_in = True  # 假设用户已登录
        if not is_logged_in:
            raise PermissionError("请先登录")
        return func(*args, **kwargs)
    return wrapper

@authenticate
def get_user_info(user_id):
    return {"id": user_id, "name": "张三"}

# 调用
get_user_info(123)
```

### 4. 缓存

```python
def memoize(func):
    cache = {}
    
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 调用
print(fibonacci(10))  # 55
```

## 内置装饰器

Python 提供了几个内置装饰器：

### @staticmethod

```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

# 使用
result = MathUtils.add(3, 5)
print(result)  # 8
```

### @classmethod

```python
class Person:
    species = "Homo sapiens"
    
    def __init__(self, name):
        self.name = name
    
    @classmethod
    def get_species(cls):
        return cls.species

# 使用
print(Person.get_species())  # Homo sapiens
```

### @property

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("半径必须大于0")
        self._radius = value
    
    @property
    def area(self):
        return 3.14159 * self._radius ** 2

# 使用
circle = Circle(5)
print(circle.radius)  # 5
print(circle.area)    # 78.53975
circle.radius = 10
print(circle.area)    # 314.159
```

## 装饰器链

可以同时使用多个装饰器：

```python
def decorator1(func):
    def wrapper(*args, **kwargs):
        print("装饰器1")
        return func(*args, **kwargs)
    return wrapper

def decorator2(func):
    def wrapper(*args, **kwargs):
        print("装饰器2")
        return func(*args, **kwargs)
    return wrapper

@decorator1
@decorator2
def hello():
    print("Hello!")

# 调用
hello()
```

**输出：**
```
装饰器1
装饰器2
Hello!
```

## 保留函数元信息

使用 `functools.wraps` 保留原函数的元信息：

```python
from functools import wraps

def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def my_function():
    """这是一个示例函数"""
    pass

print(my_function.__name__)    # my_function
print(my_function.__doc__)     # 这是一个示例函数
```

## 学习资源

- [Python 官方文档](https://docs.python.org/3/glossary.html#term-decorator)
- [菜鸟教程 Python 装饰器](https://www.runoob.com/w3cnote/python-func-decorators.html)
- [Real Python 装饰器教程](https://realpython.com/primer-on-python-decorators/)

## 总结

装饰器是 Python 中非常强大的特性，掌握装饰器可以让你的代码更加简洁、可维护和可扩展。常见的应用场景包括日志记录、性能计时、身份验证和缓存等。
""",
    
    'Vue3 组合式 API 最佳实践': """# Vue3 组合式 API 最佳实践

## 什么是组合式 API

**组合式 API** 是 Vue3 引入的新特性，提供了更灵活的代码组织方式，使得逻辑复用更加简单。

与 Vue2 的选项式 API 相比，组合式 API 有以下优势：
- 更好的代码组织
- 更好的逻辑复用
- 更好的类型推断
- 更小的生产包体积

## 核心概念

### 1. setup 函数

`setup` 是组合式 API 的入口函数：

```javascript
import { ref, reactive, computed } from 'vue';

export default {
  setup() {
    // 响应式状态
    const count = ref(0);
    const state = reactive({ name: 'Vue' });
    
    // 计算属性
    const doubled = computed(() => count.value * 2);
    
    // 方法
    const increment = () => {
      count.value++;
    };
    
    // 返回供模板使用
    return {
      count,
      state,
      doubled,
      increment
    };
  }
};
```

### 2. ref 和 reactive

**ref** 用于创建响应式的基本类型值：

```javascript
import { ref } from 'vue';

const count = ref(0);
const name = ref('张三');

// 访问值
console.log(count.value);  // 0

// 修改值
count.value++;  // count 变为 1
```

**reactive** 用于创建响应式的对象：

```javascript
import { reactive } from 'vue';

const state = reactive({
  name: '张三',
  age: 25,
  address: {
    city: '北京',
    street: '某某街道'
  }
});

// 直接访问和修改
state.name = '李四';
state.address.city = '上海';
```

**区别：**
- `ref` 需要通过 `.value` 访问和修改值
- `reactive` 可以直接访问和修改属性
- `ref` 适用于基本类型，`reactive` 适用于对象

### 3. computed 计算属性

计算属性会根据依赖自动更新：

```javascript
import { ref, computed } from 'vue';

const firstName = ref('张');
const lastName = ref('三');

// 计算属性
const fullName = computed(() => {
  return `${firstName.value}${lastName.value}`;
});

console.log(fullName.value);  // 张三

firstName.value = '李';
console.log(fullName.value);  // 李三（自动更新）
```

计算属性的特点：
- 会缓存计算结果
- 只有依赖变化时才重新计算
- 适合处理复杂的逻辑

### 4. watch 和 watchEffect

**watch** 需要明确指定依赖：

```javascript
import { ref, watch } from 'vue';

const count = ref(0);

// 监听单个值
watch(count, (newValue, oldValue) => {
  console.log(`count 从 ${oldValue} 变为 ${newValue}`);
});

// 监听多个值
const name = ref('张三');
watch([count, name], ([newCount, newName], [oldCount, oldName]) => {
  console.log(`count: ${oldCount} -> ${newCount}`);
  console.log(`name: ${oldName} -> ${newName}`);
});
```

**watchEffect** 自动追踪依赖：

```javascript
import { ref, watchEffect } from 'vue';

const count = ref(0);

watchEffect(() => {
  console.log(`count 变化了: ${count.value}`);
});

count.value++;  // 触发：count 变化了: 1
```

## 组合式函数

组合式函数是逻辑复用的核心：

```javascript
// useCounter.js
import { ref, computed } from 'vue';

export function useCounter(initialValue = 0) {
  const count = ref(initialValue);
  
  const increment = () => {
    count.value++;
  };
  
  const decrement = () => {
    count.value--;
  };
  
  const reset = () => {
    count.value = initialValue;
  };
  
  const doubled = computed(() => count.value * 2);
  
  return {
    count,
    increment,
    decrement,
    reset,
    doubled
  };
}
```

**使用组合式函数：**

```javascript
import { useCounter } from './useCounter';

export default {
  setup() {
    const { count, increment, doubled } = useCounter(10);
    
    return {
      count,
      increment,
      doubled
    };
  }
};
```

## 模板语法

```vue
<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Doubled: {{ doubled }}</p>
    <button @click="increment">+</button>
    <button @click="decrement">-</button>
    <button @click="reset">重置</button>
  </div>
</template>

<script setup>
import { useCounter } from './useCounter';

const { count, increment, decrement, reset, doubled } = useCounter(0);
</script>
```

## 响应式原理

Vue3 使用 **Proxy** 实现响应式：

```javascript
const target = { count: 0 };

const proxy = new Proxy(target, {
  get(target, key) {
    // 收集依赖
    track(target, key);
    return target[key];
  },
  set(target, key, value) {
    target[key] = value;
    // 触发更新
    trigger(target, key);
    return true;
  }
});
```

## 学习资源

- [Vue3 官方文档](https://vuejs.org/)
- [Vue 组合式 API 指南](https://vuejs.org/guide/extras/composition-api-faq.html)
- [菜鸟教程 Vue3 教程](https://www.runoob.com/vue3/vue3-tutorial.html)

## 总结

组合式 API 为 Vue3 带来了更现代的开发体验，通过 `ref`、`reactive`、`computed`、`watch` 等核心函数，可以构建更加灵活和可维护的应用。
"""
}

# 更新文章
for title, content in articles_content.items():
    article = Article.objects.filter(title=title).first()
    if article:
        article.content = content
        article.save()
        print(f"✓ 更新文章: {title}")

print("\n文章更新完成！")
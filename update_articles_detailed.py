import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_backend.settings')
django.setup()

from apps.articles.models import Article

# 更新 React 状态管理文章 - 详细版
article = Article.objects.filter(title='React 状态管理').first()
if article:
    article.content = """# React 状态管理完全指南

## 一、什么是状态管理

在开始学习 React 状态管理之前，我们首先需要理解什么是"状态"。

### 1.1 什么是状态？

**状态（State）**就是组件在某一时刻的数据。比如：

- 一个计数器组件，当前计数值就是它的状态
- 一个待办事项列表，所有待办事项就是它的状态
- 一个用户信息卡片，用户的名字、头像就是它的状态

```jsx
function Counter() {
  // count 就是一个状态
  const [count, setCount] = useState(0);
  
  return <div>当前计数：{count}</div>;
}
```

### 1.2 为什么需要状态管理？

随着应用变得复杂，我们面临以下问题：

**问题1：组件间数据传递困难**

当组件层级很深时，需要一层一层传递数据，这叫做"Props Drilling"（属性钻取）。

**问题2：状态同步困难**

多个组件需要共享同一个状态时，如何保证数据同步？

**问题3：代码难以维护**

状态分散在各个组件中，难以追踪和管理。

## 二、React 内置的状态管理方案

### 2.1 useState - 最基础的状态管理

`useState` 是 React 提供的最简单的状态管理 Hook。

#### 基本语法

```jsx
const [state, setState] = useState(initialValue);
```

**参数说明：**
- `state`：当前的状态值
- `setState`：更新状态的函数
- `initialValue`：状态的初始值

#### 示例1：计数器

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  const increment = () => {
    setCount(count + 1);
  };
  
  return (
    <div>
      <p>计数：{count}</p>
      <button onClick={increment}>+1</button>
    </div>
  );
}
```

### 2.2 useContext - 跨组件状态共享

Context 提供了一种在组件树中共享数据的方式，而不必通过每一层组件手动传递 props。

#### 使用步骤

**步骤1：创建 Context**

```jsx
import { createContext } from 'react';

const ThemeContext = createContext('light');
```

**步骤2：提供 Context**

```jsx
<ThemeContext.Provider value="dark">
  <Header />
</ThemeContext.Provider>
```

**步骤3：消费 Context**

```jsx
import { useContext } from 'react';

function Header() {
  const theme = useContext(ThemeContext);
  return <nav>主题：{theme}</nav>;
}
```

## 三、第三方状态管理库

### 3.1 Redux - 最流行的状态管理库

Redux 是一个可预测的状态容器，适用于 JavaScript 应用。

#### 安装

```bash
npm install redux react-redux @reduxjs/toolkit
```

#### 核心概念

Redux 有三个核心概念：

1. **Store（存储）**：保存整个应用的状态
2. **Action（动作）**：描述发生了什么
3. **Reducer（归约器）**：根据 action 更新状态

#### 基本使用

**创建 Slice：**

```jsx
import { createSlice } from '@reduxjs/toolkit';

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => { state.value += 1; },
    decrement: (state) => { state.value -= 1; },
  },
});

export const { increment, decrement } = counterSlice.actions;
export default counterSlice.reducer;
```

**配置 Store：**

```jsx
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './counterSlice';

export const store = configureStore({
  reducer: { counter: counterReducer },
});
```

**在组件中使用：**

```jsx
import { useSelector, useDispatch } from 'react-redux';
import { increment, decrement } from './counterSlice';

function Counter() {
  const count = useSelector((state) => state.counter.value);
  const dispatch = useDispatch();
  
  return (
    <div>
      <p>计数：{count}</p>
      <button onClick={() => dispatch(increment())}>+1</button>
      <button onClick={() => dispatch(decrement())}>-1</button>
    </div>
  );
}
```

### 3.2 Zustand - 轻量级状态管理

Zustand 是一个轻量级的状态管理库，API 简洁易用。

#### 安装

```bash
npm install zustand
```

#### 基本使用

```jsx
import create from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));

function Counter() {
  const count = useStore((state) => state.count);
  const increment = useStore((state) => state.increment);
  
  return (
    <div>
      <p>计数：{count}</p>
      <button onClick={increment}>+1</button>
    </div>
  );
}
```

## 四、如何选择合适的状态管理方案

| 方案 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| useState | 简单组件状态 | 轻量、易用 | 不适合跨组件共享 |
| useContext | 中等规模应用 | 减少 props 传递 | 可能导致不必要渲染 |
| Redux | 大型复杂应用 | 强大、可预测 | 学习曲线较陡 |
| Zustand | 中小型应用 | 轻量、API简洁 | 生态较小 |

### 选择建议

1. **小型项目**：使用 `useState` 和 `useContext`
2. **中型项目**：考虑使用 `Zustand`
3. **大型项目**：使用 `Redux`

## 五、学习资源

- [React 官方文档](https://react.dev/) - 最权威的 React 学习资料
- [菜鸟教程 React 教程](https://www.runoob.com/react/react-tutorial.html) - 适合初学者的中文教程
- [Redux 官方文档](https://redux.js.org/) - Redux 官方文档
- [Zustand 官方文档](https://docs.pmnd.rs/zustand) - Zustand 官方文档

## 六、总结

状态管理是 React 开发中的核心概念，选择合适的方案取决于项目规模和复杂度。

记住：**没有最好的状态管理方案，只有最适合的方案**。
"""
    article.save()
    print('✓ 更新 React 状态管理文章（详细版）')

# 更新 Python 装饰器文章 - 详细版
article = Article.objects.filter(title='Python 装饰器完全指南').first()
if article:
    article.content = """# Python 装饰器完全指南

## 一、什么是装饰器

**装饰器（Decorator）**是 Python 中一种强大的语法特性，它允许在不修改函数代码的情况下扩展函数功能。

### 1.1 装饰器的本质

装饰器本质上是一个**高阶函数**，它接受一个函数作为参数，并返回一个新的函数。

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

### 1.2 为什么需要装饰器？

装饰器的作用类似于"包装"，可以在不修改原函数的情况下，为函数添加额外的功能。

**应用场景：**
- 日志记录
- 性能计时
- 身份验证
- 缓存
- 事务处理

## 二、装饰器的基本语法

### 2.1 简单装饰器

```python
def my_decorator(func):
    def wrapper():
        print("装饰器：开始执行")
        func()
        print("装饰器：执行完成")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```

### 2.2 带参数的装饰器

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")

say_hello()
```

**输出：**
```
Hello!
Hello!
Hello!
```

## 三、装饰器的应用场景

### 3.1 日志记录

```python
def log(func):
    def wrapper(*args, **kwargs):
        print(f"调用函数：{func.__name__}")
        print(f"参数：args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"返回值：{result}")
        return result
    return wrapper

@log
def add(a, b):
    return a + b

add(3, 5)
```

### 3.2 性能计时

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 耗时：{end_time - start_time:.4f}秒")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(2)
    print("函数执行完成")

slow_function()
```

### 3.3 身份验证

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

get_user_info(123)
```

## 四、内置装饰器

Python 提供了几个内置装饰器：

### 4.1 @staticmethod

```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

result = MathUtils.add(3, 5)
print(result)  # 8
```

### 4.2 @classmethod

```python
class Person:
    species = "Homo sapiens"
    
    @classmethod
    def get_species(cls):
        return cls.species

print(Person.get_species())  # Homo sapiens
```

### 4.3 @property

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

circle = Circle(5)
print(circle.radius)  # 5
print(circle.area)    # 78.53975
```

## 五、学习资源

- [Python 官方文档](https://docs.python.org/3/)
- [菜鸟教程 Python](https://www.runoob.com/python/python-tutorial.html)
- [Real Python 装饰器教程](https://realpython.com/primer-on-python-decorators/)

## 六、总结

装饰器是 Python 中非常强大的特性，掌握装饰器可以让你的代码更加简洁、可维护和可扩展。
"""
    article.save()
    print('✓ 更新 Python 装饰器文章（详细版）')

# 更新 Vue3 组合式 API 文章 - 详细版
article = Article.objects.filter(title='Vue3 组合式 API 最佳实践').first()
if article:
    article.content = """# Vue3 组合式 API 最佳实践

## 一、什么是组合式 API

**组合式 API** 是 Vue3 引入的新特性，提供了更灵活的代码组织方式，使得逻辑复用更加简单。

### 1.1 为什么需要组合式 API？

Vue2 的选项式 API（Options API）将代码按照 `data`、`methods`、`computed` 等选项组织，这在简单应用中很方便，但在复杂应用中会导致相关逻辑分散。

**问题示例：**

```javascript
// Vue2 选项式 API
export default {
  data() {
    return {
      count: 0,
      name: 'Vue',
      age: 25
    }
  },
  computed: {
    doubled() {
      return this.count * 2
    }
  },
  methods: {
    increment() {
      this.count++
    }
  }
}
```

### 1.2 组合式 API 的优势

1. **更好的代码组织** - 相关逻辑可以组织在一起
2. **更好的逻辑复用** - 可以创建可复用的组合函数
3. **更好的类型推断** - 对 TypeScript 更友好
4. **更小的生产包体积** - 摇树优化更有效

## 二、核心概念

### 2.1 setup 函数

`setup` 是组合式 API 的入口函数，在组件创建之前执行。

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

### 2.2 ref 和 reactive

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

### 2.3 computed 计算属性

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

### 2.4 watch 和 watchEffect

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

## 三、组合式函数

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

## 四、学习资源

- [Vue3 官方文档](https://vuejs.org/)
- [Vue 组合式 API 指南](https://vuejs.org/guide/extras/composition-api-faq.html)
- [菜鸟教程 Vue3](https://www.runoob.com/vue3/vue3-tutorial.html)

## 五、总结

组合式 API 为 Vue3 带来了更现代的开发体验，通过 `ref`、`reactive`、`computed`、`watch` 等核心函数，可以构建更加灵活和可维护的应用。
"""
    article.save()
    print('✓ 更新 Vue3 组合式 API 文章（详细版）')

print('\n所有文章更新完成！')
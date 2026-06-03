import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_backend.settings')
django.setup()

from django.contrib.auth.models import User
from apps.articles.models import Article

def add_sample_data():
    print("正在创建示例数据...")
    
    # 创建超级用户（如果不存在）
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✓ 创建超级用户: admin")
    else:
        print("- 超级用户已存在: admin")

    # 创建示例文章
    sample_articles = [
        {
            'title': 'Python 装饰器完全指南',
            'content': '''# Python 装饰器完全指南

## 什么是装饰器？

装饰器是 Python 的一个重要特性，它允许我们在不修改原函数代码的情况下，为函数添加额外的功能。

### 基础概念

装饰器本质上是一个函数，它接受另一个函数作为参数，并返回一个新的函数。

```python
def my_decorator(func):
    def wrapper():
        print("函数执行前")
        func()
        print("函数执行后")
    return wrapper

@my_decorator
def say_hello():
    print("Hello, World!")

say_hello()
```

输出：
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
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
```

### 实际应用示例

#### 1. 计时装饰器

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.2f} 秒")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "完成"

slow_function()
```

#### 2. 认证装饰器

```python
def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 这里可以检查用户是否已认证
        authenticated = True  # 简化示例
        if not authenticated:
            raise PermissionError("需要认证才能访问")
        return func(*args, **kwargs)
    return wrapper

@require_auth
def sensitive_data():
    return "敏感数据"

sensitive_data()
```

## 学习资源

- [Python 官方文档](https://docs.python.org/3/)
- [Real Python 装饰器教程](https://realpython.com/primer-on-python-decorators/)
- [菜鸟教程 Python](https://www.runoob.com/python3/python3-tutorial.html)
''',
            'status': 'published'
        },
        {
            'title': 'React 状态管理完全指南',
            'content': '''# React 状态管理完全指南

## 什么是状态管理？

在 React 应用中，状态管理是指管理和维护应用数据的过程。随着应用复杂性的增加，有效的状态管理变得至关重要。

### React 内置状态管理

#### 1. useState Hook

```jsx
import React, { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>计数: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        增加
      </button>
      <button onClick={() => setCount(0)}>
        重置
      </button>
    </div>
  );
}

export default Counter;
```

#### 2. useReducer Hook

```jsx
import React, { useReducer } from 'react';

const initialState = { count: 0 };

function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    case 'reset':
      return initialState;
    default:
      throw new Error();
  }
}

function CounterWithReducer() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <div>
      <p>计数: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>
        +
      </button>
      <button onClick={() => dispatch({ type: 'decrement' })}>
        -
      </button>
      <button onClick={() => dispatch({ type: 'reset' })}>
        重置
      </button>
    </div>
  );
}

export default CounterWithReducer;
```

#### 3. useContext Hook

```jsx
import React, { useContext, useState } from 'react';

const CountContext = React.createContext();

function CountProvider({ children }) {
  const [count, setCount] = useState(0);

  return (
    <CountContext.Provider value={{ count, setCount }}>
      {children}
    </CountContext.Provider>
  );
}

function DisplayCount() {
  const { count } = useContext(CountContext);
  return <div>当前计数: {count}</div>;
}

function IncrementButton() {
  const { count, setCount } = useContext(CountContext);
  return (
    <button onClick={() => setCount(count + 1)}>
      增加计数
    </button>
  );
}

function App() {
  return (
    <CountProvider>
      <DisplayCount />
      <IncrementButton />
    </CountProvider>
  );
}
```

### 第三方状态管理库

#### 1. Redux Toolkit

```jsx
// store.js
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './counterSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
  },
});

// counterSlice.js
import { createSlice } from '@reduxjs/toolkit';

export const counterSlice = createSlice({
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

// Component.jsx
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { increment, decrement } from './counterSlice';

function Counter() {
  const count = useSelector((state) => state.counter.value);
  const dispatch = useDispatch();

  return (
    <div>
      <span>{count}</span>
      <button onClick={() => dispatch(increment())}>+</button>
      <button onClick={() => dispatch(decrement())}>-</button>
    </div>
  );
}
```

#### 2. Zustand (轻量级替代方案)

```jsx
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));

function Counter() {
  const { count, increment, decrement, reset } = useStore();

  return (
    <div>
      <p>计数: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
      <button onClick={reset}>重置</button>
    </div>
  );
}
```

### 状态管理最佳实践

1. **状态提升**: 当多个组件需要共享状态时，将其提升到最近的共同祖先组件

2. **单一数据源**: 尽可能将相关的状态集中管理

3. **不可变性**: 不要直接修改状态，而是创建新的状态对象

4. **状态分层**: 对于大型应用，考虑将状态分为 UI 状态和业务状态

5. **性能优化**: 使用 React.memo、useMemo 和 useCallback 避免不必要的重渲染

## 学习资源

- [React 官方文档](https://react.dev/)
- [Redux Toolkit 文档](https://redux-toolkit.js.org/)
- [Zustand 文档](https://docs.pmnd.rs/zustand/getting-started/introduction)
- [菜鸟教程 React](https://www.runoob.com/react/react-tutorial.html)
''',
            'status': 'published'
        },
        {
            'title': 'Vue3 组合式 API 最佳实践',
            'content': '''# Vue3 组合式 API 最佳实践

## 什么是组合式 API？

组合式 API (Composition API) 是 Vue3 引入的一种新的 API 风格，它允许我们更灵活地组织和重用组件逻辑。

### 基础概念

#### 1. setup() 函数

setup() 是组合式 API 的入口点，在组件创建之前执行：

```vue
<template>
  <div>
    <p>计数: {{ count }}</p>
    <p>双倍计数: {{ doubleCount }}</p>
    <button @click="increment">增加</button>
  </div>
</template>

<script>
import { ref, computed } from 'vue';

export default {
  setup() {
    // 响应式数据
    const count = ref(0);
    
    // 计算属性
    const doubleCount = computed(() => count.value * 2);
    
    // 方法
    const increment = () => {
      count.value++;
    };
    
    // 暴露给模板
    return {
      count,
      doubleCount,
      increment
    };
  }
};
</script>
```

#### 2. &lt;script setup&gt; 语法糖

Vue3 提供了更简洁的语法：

```vue
<template>
  <div>
    <p>计数: {{ count }}</p>
    <p>双倍计数: {{ doubleCount }}</p>
    <button @click="increment">增加</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const count = ref(0);
const doubleCount = computed(() => count.value * 2);

const increment = () => {
  count.value++;
};
</script>
```

### 常用组合式 API

#### 1. 响应式 API

```javascript
import { ref, reactive, toRefs, computed, watch, watchEffect } from 'vue';

// ref: 创建响应式基本类型
const count = ref(0);

// reactive: 创建响应式对象
const state = reactive({
  name: 'Vue',
  version: 3
});

// computed: 计算属性
const fullName = computed(() => `${state.firstName} ${state.lastName}`);

// watch: 监听响应式数据变化
watch(count, (newVal, oldVal) => {
  console.log(`计数从 ${oldVal} 变为 ${newVal}`);
});

// watchEffect: 自动追踪依赖
watchEffect(() => {
  console.log(`当前计数: ${count.value}`);
});
```

#### 2. 生命周期钩子

```javascript
import { 
  onMounted, 
  onUpdated, 
  onUnmounted, 
  onBeforeMount,
  onBeforeUpdate,
  onBeforeUnmount
} from 'vue';

export default {
  setup() {
    onMounted(() => {
      console.log('组件已挂载');
    });
    
    onUpdated(() => {
      console.log('组件已更新');
    });
    
    onUnmounted(() => {
      console.log('组件即将卸载');
    });
    
    return {};
  }
};
```

### 自定义组合函数

组合式 API 的强大之处在于可以创建可重用的逻辑：

```javascript
// composables/useCounter.js
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
  
  const doubleCount = computed(() => count.value * 2);
  
  return {
    count,
    increment,
    decrement,
    reset,
    doubleCount
  };
}

// 在组件中使用
<template>
  <div>
    <p>计数: {{ count }}</p>
    <p>双倍: {{ doubleCount }}</p>
    <button @click="increment">+</button>
    <button @click="decrement">-</button>
    <button @click="reset">重置</button>
  </div>
</template>

<script setup>
import { useCounter } from '@/composables/useCounter';

const { count, increment, decrement, reset, doubleCount } = useCounter(10);
</script>
```

### 状态管理

#### 1. Pinia (Vue3 官方推荐)

```javascript
// stores/counter.js
import { defineStore } from 'pinia';

export const useCounterStore = defineStore('counter', {
  // 状态
  state: () => ({
    count: 0,
    name: 'Vue Counter'
  }),
  
  // 计算属性
  getters: {
    doubleCount: (state) => state.count * 2,
    doubleCountPlusOne: (state) => state.doubleCount + 1
  },
  
  // 动作
  actions: {
    increment() {
      this.count++;
    },
    incrementBy(amount) {
      this.count += amount;
    },
    async fetchData() {
      // 异步操作
      const response = await fetch('/api/data');
      const data = await response.json();
      this.items = data;
    }
  }
});

// 在组件中使用
<template>
  <div>
    <p>{{ store.count }} - {{ store.doubleCount }}</p>
    <button @click="store.increment()">增加</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
</script>
```

### 最佳实践

#### 1. 组织代码逻辑

```javascript
// composables/useUserData.js
import { ref, computed, onMounted } from 'vue';
import { getUserById } from '@/api/user';

export function useUserData(userId) {
  const user = ref(null);
  const loading = ref(false);
  const error = ref(null);
  
  const userName = computed(() => user.value?.name || '');
  const userAvatar = computed(() => user.value?.avatar || '');
  
  const fetchUser = async () => {
    loading.value = true;
    error.value = null;
    
    try {
      user.value = await getUserById(userId);
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };
  
  onMounted(fetchUser);
  
  return {
    user,
    loading,
    error,
    userName,
    userAvatar,
    fetchUser
  };
}
```

#### 2. 类型安全 (使用 TypeScript)

```typescript
// composables/useApi.ts
import { ref, Ref } from 'vue';

interface ApiResponse<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

export function useApi<T>(apiCall: () => Promise<T>): ApiResponse<T> {
  const data: Ref<T | null> = ref(null);
  const loading = ref(false);
  const error = ref<string | null>(null);
  
  const execute = async () => {
    loading.value = true;
    error.value = null;
    
    try {
      data.value = await apiCall();
    } catch (err: any) {
      error.value = err.message || 'An error occurred';
    } finally {
      loading.value = false;
    }
  };
  
  return {
    data,
    loading,
    error,
    execute
  };
}
```

### 性能优化

#### 1. 避免不必要的响应式开销

```javascript
import { shallowRef, triggerRef } from 'vue';

// 对于大型不可变数据，使用浅层响应式
const largeData = shallowRef([]);
largeData.value = newData; // 只有引用改变时才触发更新
triggerRef(largeData); // 手动触发更新
```

#### 2. 正确使用 v-memo

```vue
<template>
  <!-- 优化列表渲染 -->
  <div v-for="item in list" :key="item.id" v-memo="[item.id, item.selected]">
    <ListItem :item="item" />
  </div>
</template>
```

## 学习资源

- [Vue3 官方文档](https://vuejs.org/)
- [Pinia 文档](https://pinia.vuejs.org/)
- [Vue3 组合式 API 介绍](https://vuejs.org/guide/extras/composition-api-faq.html)
- [菜鸟教程 Vue3](https://www.runoob.com/vue3/vue3-tutorial.html)
''',
            'status': 'published'
        }
    ]

    created_count = 0
    for article_data in sample_articles:
        article, created = Article.objects.get_or_create(
            title=article_data['title'],
            defaults={
                'author': admin_user,
                'content': article_data['content'],
                'status': article_data['status']
            }
        )
        if created:
            print(f"✓ 创建文章: {article.title}")
            created_count += 1
        else:
            print(f"- 文章已存在: {article.title}")

    print(f"\n✅ 完成！共创建了 {created_count} 篇示例文章")
    print("现在您可以访问网站查看这些文章了")

if __name__ == "__main__":
    add_sample_data()
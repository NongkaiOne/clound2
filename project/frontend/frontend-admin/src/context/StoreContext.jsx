import { createContext, useContext, useState } from 'react'
import { mockStores, mockAreas } from '../data/mockData'

const StoreContext = createContext()

export function StoreProvider({ children }) {
    const [stores, setStores] = useState(mockStores)
    const [areas, setAreas] = useState(mockAreas)

    return (
        <StoreContext.Provider value={{ stores, setStores, areas, setAreas }}>
            {children}
        </StoreContext.Provider>
    )
}

export function useStores() {
    return useContext(StoreContext)
}
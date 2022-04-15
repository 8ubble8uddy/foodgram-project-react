import styles from './style.module.css'
import { useContext } from 'react'
import { Container, LinkComponent } from '../index'
import { UserContext, AuthContext } from '../../contexts'

const Footer = () => {
  const authContext = useContext(AuthContext)
  const userContext = useContext(UserContext)
  return <footer className={styles.footer}>
      <Container className={styles.footer__container}>
        {<LinkComponent
          href={authContext ? `/user/${userContext.id}` : '/signin'}
          title='Твои рецепты'
          className={styles.footer__brand} 
        />}
      </Container>
  </footer>
}

export default Footer

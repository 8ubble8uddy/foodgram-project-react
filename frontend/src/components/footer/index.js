import styles from './style.module.css'
import { useContext } from 'react'
import { Container, LinkComponent } from '../index'
import { UserContext } from '../../contexts'

const Footer = () => {
  const userContext = useContext(UserContext)
  return <footer className={styles.footer}>
      <Container className={styles.footer__container}>
        <LinkComponent
          href={`/user/${userContext.id}`}
          title={`${userContext.username}`}
          className={styles.footer__brand} 
        />
      </Container>
  </footer>
}

export default Footer
